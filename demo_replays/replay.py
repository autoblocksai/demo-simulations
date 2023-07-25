import argparse

import requests
from autoblocks.replays import replay_events_from_view
from autoblocks.replays import start_replay

from demo_replays.settings import AUTOBLOCKS_REPLAYS_TRACE_ID_PARAM_NAME
from demo_replays.settings import env


def static():
    """
    Replays a static set of events against the locally-running app.
    """
    start_replay()

    for trace_id, query in [
        ("sf", "San Francisco tourist attractions"),
        ("paris", "Paris tourist attractions"),
        ("lombard", "Lombard Street"),
        ("eiffel", "Eiffel Tower"),
    ]:
        print(f"Testing static event {trace_id} - {query}")
        requests.post("http://localhost:5000", json={AUTOBLOCKS_REPLAYS_TRACE_ID_PARAM_NAME: trace_id, "query": query})


def dynamic():
    """
    Replays a dynamic set of events fetched from the Autoblocks API against the locally-running app.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--view-id", help="The view to replay events from", required=True, type=str)
    parser.add_argument(
        "--num-traces",
        help="The number of traces to replay from the view",
        required=True,
        type=int,
    )
    args = parser.parse_args()

    start_replay()

    for event in replay_events_from_view(
        api_key=env.AUTOBLOCKS_API_KEY,
        view_id=args.view_id,
        num_traces=args.num_traces,
    ):
        if event.message == "request.payload":
            print(f"Replaying past event {event}")

            # The original payload
            payload = event.properties["payload"]

            # Modify the payload to pass in the replay trace id
            payload[AUTOBLOCKS_REPLAYS_TRACE_ID_PARAM_NAME] = event.trace_id

            # Replay the request
            requests.post("http://localhost:5000", json=payload)
