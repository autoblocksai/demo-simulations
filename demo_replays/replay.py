import argparse

import requests
from autoblocks.api.client import AutoblocksAPIClient

from demo_replays.settings import AUTOBLOCKS_REPLAY_TRACE_ID_HEADER_NAME
from demo_replays.settings import env


def static():
    """
    Replays a static set of events against the locally-running app.
    """
    for trace_id, query in [
        ("san-francisco-tourist-attractions", "San Francisco tourist attractions"),
        ("paris-tourist-attractions", "Paris tourist attractions"),
        ("lombard-stree", "Lombard Street"),
        ("eiffel-tower", "Eiffel Tower"),
    ]:
        print(f"Testing static event {trace_id} - {query}")
        requests.post(
            "http://localhost:5000",
            json={"query": query},
            headers={AUTOBLOCKS_REPLAY_TRACE_ID_HEADER_NAME: trace_id},
        )


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

    ab_client = AutoblocksAPIClient(env.AUTOBLOCKS_API_KEY)

    resp = ab_client.get_traces_from_view(view_id=args.view_id, page_size=args.num_traces)
    for trace in resp.traces:
        for event in trace.events:
            if event.message == "request.payload":
                print(f"Replaying past event {event}")

                # The original payload
                payload = event.properties["payload"]

                # Replay the request
                requests.post(
                    "http://localhost:5000",
                    json=payload,
                    headers={AUTOBLOCKS_REPLAY_TRACE_ID_HEADER_NAME: event.trace_id},
                )
