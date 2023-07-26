from pydantic_settings import BaseSettings

# A hidden param that is used to override the trace id that would usually
# be randomly generated for each request with the trace id of the event
# that is being replayed
AUTOBLOCKS_REPLAYS_TRACE_ID_PARAM_NAME = "__autoblocks_replay_trace_id"


# Environment variables
class Env(BaseSettings):
    # Autoblocks secrets
    AUTOBLOCKS_API_KEY: str = ""
    AUTOBLOCKS_INGESTION_KEY: str = ""

    # OpenAI secrets
    OPENAI_API_KEY: str = ""


env = Env()
