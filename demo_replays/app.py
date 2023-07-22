import uuid

from flask import Flask
from flask import request

from demo_replays import bot
from demo_replays.autoblocks_sdk import AutoblocksLogger
from demo_replays.settings import settings

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
    trace_id = payload.get(settings.AUTOBLOCKS_REPLAYS_TRACE_ID_PARAM_NAME) or str(uuid.uuid4())

    autoblocks = AutoblocksLogger(
        ingestion_key=settings.AUTOBLOCKS_INGESTION_KEY,
        trace_id=trace_id,
        source="DEMO_REPLAYS",
    )
    autoblocks.send_event("request.payload", {"payload": payload})

    output = bot.get_response(autoblocks, query)

    response = {"output": output}
    autoblocks.send_event("request.response", {"response": response})

    return response


def start():
    app.run(debug=True)
