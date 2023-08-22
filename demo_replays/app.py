import uuid

from autoblocks.tracer import AutoblocksTracer
from flask import Flask
from flask import request

from demo_replays import bot
from demo_replays.settings import AUTOBLOCKS_REPLAY_TRACE_ID_HEADER_NAME
from demo_replays.settings import REQUEST_PAYLOAD_MESSAGE
from demo_replays.settings import env

app = Flask(__name__)


@app.route("/health")
def hello_world():
    return {"status": "ok"}


@app.route("/", methods=["POST"])
def main():
    payload = request.get_json()
    # Input from the user
    query = payload.get("query")
    if not query:
        return "query is required", 400

    # In production we generate a new trace id for each request,
    # but in a replay scenario we use the trace id passed in from the replay
    trace_id = request.headers.get(AUTOBLOCKS_REPLAY_TRACE_ID_HEADER_NAME) or str(uuid.uuid4())

    autoblocks = AutoblocksTracer(
        env.AUTOBLOCKS_INGESTION_KEY,
        trace_id=trace_id,
        properties=dict(source="DEMO_REPLAYS"),
    )
    autoblocks.send_event(REQUEST_PAYLOAD_MESSAGE, properties=dict(payload=payload))

    output = bot.get_response(autoblocks, query)

    response = {"output": output}
    autoblocks.send_event("request.response", properties=dict(response=response))

    return response


def start():
    import logging

    logging.basicConfig(filename="flask.log", level=logging.DEBUG)
    app.run(debug=True)
