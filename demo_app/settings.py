from pydantic_settings import BaseSettings

# When a request is from a simulation, this header contains the trace ID of
# the event being handled during the simulation.
AUTOBLOCKS_SIMULATION_TRACE_ID_HEADER_NAME = "x-autoblocks-simulation-trace-id"

# The message for the user input event, pulled into a variable here
# so that it's kept in sync between sending the events and replaying them.
USER_QUERY_MESSAGE = "user.query"


# Environment variables
class Env(BaseSettings):
    # Autoblocks secrets
    AUTOBLOCKS_API_KEY: str = ""
    AUTOBLOCKS_INGESTION_KEY: str = ""

    # OpenAI secrets
    OPENAI_API_KEY: str = ""


env = Env()
