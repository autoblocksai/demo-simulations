import argparse
from datetime import datetime

import requests

from demo_replays.autoblocks_sdk import replay_events_from_view
from demo_replays.settings import settings


def main():
    """
    Replays events against the locally-running app.
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

    replay_id = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    print("#" * 80)
    print(f"Your replay id is {replay_id}")
    print("#" * 80)
    print()

    for event in replay_events_from_view(
        api_key=settings.AUTOBLOCKS_API_KEY,
        replay_id=replay_id,
        view_id=args.view_id,
        num_traces=args.num_traces,
    ):
        if event["message"] == "request.payload":
            print(f"Replaying event {event}")

            # The original payload
            payload = event["properties"]["payload"]

            # Modify the payload to pass in the replay trace id
            payload[settings.AUTOBLOCKS_REPLAYS_TRACE_ID_PARAM_NAME] = event["traceId"]

            # Replay the request
            requests.post("http://localhost:5000", json=payload)
