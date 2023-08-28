import requests
from autoblocks.api.client import AutoblocksAPIClient
from autoblocks.api.models import EventFilter
from autoblocks.api.models import EventFilterOperator
from autoblocks.api.models import RelativeTimeFilter
from autoblocks.api.models import SystemEventFilterKey
from autoblocks.api.models import TraceFilter
from autoblocks.api.models import TraceFilterOperator

from demo_app.settings import AUTOBLOCKS_SIMULATION_TRACE_ID_HEADER_NAME
from demo_app.settings import REQUEST_PAYLOAD_MESSAGE
from demo_app.settings import env


def static():
    """
    Test a static set of events against the locally-running app.
    """
    for trace_id, query in [
        ("san-francisco-tourist-attractions", "San Francisco tourist attractions"),
        ("paris-tourist-attractions", "Paris tourist attractions"),
        ("lombard-street", "Lombard Street"),
        ("eiffel-tower", "Eiffel Tower"),
    ]:
        print(f"Testing static event {trace_id} - {query}")
        requests.post(
            "http://localhost:5000",
            json={"query": query},
            headers={AUTOBLOCKS_SIMULATION_TRACE_ID_HEADER_NAME: trace_id},
        )


def production_replay():
    """
    Replays production events fetched from the Autoblocks API against the locally-running app.
    """
    ab_client = AutoblocksAPIClient(env.AUTOBLOCKS_API_KEY)

    page = ab_client.search_traces(
        page_size=3,
        time_filter=RelativeTimeFilter(years=1),
        trace_filters=[
            TraceFilter(
                operator=TraceFilterOperator.CONTAINS,
                event_filters=[
                    EventFilter(
                        key=SystemEventFilterKey.MESSAGE,
                        operator=EventFilterOperator.EQUALS,
                        value=REQUEST_PAYLOAD_MESSAGE,
                    ),
                ],
            ),
        ],
    )
    for trace in page.traces:
        for event in trace.events:
            if event.message == REQUEST_PAYLOAD_MESSAGE:
                print(f"Replaying past event {event}")

                # The original payload
                payload = event.properties["payload"]

                # Replay the request
                requests.post(
                    "http://localhost:5000",
                    json=payload,
                    headers={AUTOBLOCKS_SIMULATION_TRACE_ID_HEADER_NAME: event.trace_id},
                )
