"""
This file simulates what we will provide via the Autoblocks Python SDK.
"""
import json
import os
from enum import StrEnum
from typing import Iterator
from typing import Optional

import requests
from pydantic_settings import BaseSettings

# Endpoints
INGESTION_ENDPOINT = "https://ingest-event.autoblocks.ai"
API_ENDPOINT = "https://api.autoblocks.ai"


class Settings(BaseSettings):
    """
    Settings for the Autoblocks SDK that are controlled by users via environment variables.
    """

    # `CI` will be set to true in most CI environments, e.g. GitHub Actions, GitLab, Jenkins, etc.
    CI: bool = False

    # Users should set this to true to enable replaying events
    AUTOBLOCKS_REPLAYS_ENABLED: bool = False

    # The directory where we store the replayed events in local environments
    AUTOBLOCKS_REPLAYS_DIRECTORY: str = "autoblocks-replays"

    # The file where we store the replayed events in CI environments
    AUTOBLOCKS_REPLAYS_FILEPATH: str = "replays.json"


settings = Settings()


class EventType(StrEnum):
    ORIGINAL = "original"
    REPLAYED = "replayed"


def _convert_numbers_to_strings(d: dict) -> dict:
    out = {}
    for k, v in d.items():
        if isinstance(v, dict):
            out[k] = _convert_numbers_to_strings(v)
        elif isinstance(v, list):
            out[k] = [_convert_numbers_to_strings(item) for item in v]
        elif isinstance(v, (int, float)):
            out[k] = str(v)
        else:
            out[k] = v
    return out


def _write_event_to_file_ci(
    trace_id: str,
    message: str,
    properties: Optional[dict] = None,
) -> None:
    """
    In CI environments we just write all the traces to one file. This makes it
    a bit easier for the downstream job to process the replayed traces.
    """
    # If the replays file doesn't exist, create it
    if not os.path.exists(settings.AUTOBLOCKS_REPLAYS_FILEPATH):
        with open(settings.AUTOBLOCKS_REPLAYS_FILEPATH, "w") as f:
            f.write(json.dumps([]))

    # Read the file and append the new event
    with open(settings.AUTOBLOCKS_REPLAYS_FILEPATH, "r") as f:
        content = json.loads(f.read())

    with open(settings.AUTOBLOCKS_REPLAYS_FILEPATH, "w") as f:
        content.append(
            {
                "message": message,
                "traceId": trace_id,
                "properties": _convert_numbers_to_strings(properties),
            }
        )
        f.write(json.dumps(content, indent=2, sort_keys=True))


def _write_event_to_file_local(
    event_type: EventType,
    trace_id: str,
    message: str,
    replay_id: Optional[str] = None,
    properties: Optional[dict] = None,
) -> None:
    """
    In local environments we write the replayed events to a directory structure
    that looks like this:

    autoblocks-replays/
        <replay-id>/
            <trace-id>/
                original/
                    <event-number>-<message>.json
                replayed/
                    <event-number>-<message>.json
    """
    # Assume the last folder in the replay directory is the current replay folder
    # if not explicitly specified
    replay_id = replay_id or sorted(os.listdir(settings.AUTOBLOCKS_REPLAYS_DIRECTORY))[-1]

    directory = os.path.join(
        settings.AUTOBLOCKS_REPLAYS_DIRECTORY,
        replay_id,
        trace_id,
        event_type,
    )

    os.makedirs(directory, exist_ok=True)

    num_existing_replayed_events = len(os.listdir(directory))

    filename = os.path.join(
        directory,
        # Prefix with the replay number so that the replayed files are sorted
        # by replay order
        f"{num_existing_replayed_events + 1}-{message.replace(' ', '-')}.json",
    )

    with open(filename, "w") as f:
        f.write(
            json.dumps(
                {
                    "message": message,
                    "properties": _convert_numbers_to_strings(properties),
                },
                indent=2,
                sort_keys=True,
            )
        )


def replay_events_from_view(*, api_key: str, replay_id: str, view_id: str, num_traces: int) -> Iterator[dict]:
    req = requests.get(
        f"{API_ENDPOINT}/views/{view_id}/traces",
        params={
            "pageSize": num_traces,
        },
        headers={
            "Authorization": f"Bearer {api_key}",
        },
    )
    req.raise_for_status()
    response = req.json()

    for trace in response["traces"]:
        for event in trace["events"]:
            _write_event_to_file_local(
                replay_id=replay_id,
                event_type=EventType.ORIGINAL,
                trace_id=trace["id"],
                message=event["message"],
                properties=event["properties"],
            )
            yield event


class AutoblocksLogger:
    def __init__(self, *, ingestion_key: str, trace_id: str, source: Optional[str] = None):
        self._ingestion_key = ingestion_key
        self._trace_id = trace_id
        self._source = source

    def send_event(self, message: str, properties: Optional[dict] = None) -> None:
        properties = properties or {}
        if self._source:
            properties["source"] = self._source

        if settings.AUTOBLOCKS_REPLAYS_ENABLED:
            if settings.CI:
                _write_event_to_file_ci(
                    trace_id=self._trace_id,
                    message=message,
                    properties=properties,
                )
            else:
                _write_event_to_file_local(
                    event_type=EventType.REPLAYED,
                    trace_id=self._trace_id,
                    message=message,
                    properties=properties,
                )
            return

        requests.post(
            INGESTION_ENDPOINT,
            json={
                "message": message,
                "traceId": self._trace_id,
                "properties": properties,
            },
            headers={
                "Authorization": f"Bearer {self._ingestion_key}",
            },
            timeout=5,
        )
