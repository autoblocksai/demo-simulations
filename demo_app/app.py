import uuid

from flask import Flask
from flask import request

from demo_app import bot
from demo_app.settings import AUTOBLOCKS_SIMULATION_TRACE_ID_HEADER_NAME

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
    # but in a simulation scenario we use the trace id passed in via the simulation trace id header
    trace_id = request.headers.get(AUTOBLOCKS_SIMULATION_TRACE_ID_HEADER_NAME) or str(uuid.uuid4())

    output = bot.get_response(trace_id, query)

    return dict(output=output)


def start():
    import logging

    logging.basicConfig(filename="flask.log", level=logging.DEBUG)
    app.run(debug=True)
