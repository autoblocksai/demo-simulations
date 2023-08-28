import pytest

from demo_app import bot


@pytest.mark.parametrize(
    "trace_id,query,expected_output",
    [
        ("san-francisco-tourist-attractions", "San Francisco tourist attractions", "Lombard"),
        ("paris-tourist-attractions", "Paris tourist attractions", "Eiffel"),
        ("lombard-street", "Lombard Street", "San Francisco"),
        ("eiffel-tower", "Eiffel Tower", "Paris"),
    ],
)
def test_bot(trace_id: str, query: str, expected_output: str):
    response = bot.get_response(trace_id, query)
    assert expected_output in response
