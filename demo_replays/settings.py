from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Autoblocks secrets
    AUTOBLOCKS_API_KEY: str = ""
    AUTOBLOCKS_INGESTION_KEY: str = ""

    # A hidden param that is used to override the trace id that would usually
    # be randomly generated for each request with the trace id of the event
    # that is being replayed
    AUTOBLOCKS_REPLAYS_TRACE_ID_PARAM_NAME: str = "__autoblocks_replay_trace_id"

    # OpenAI secrets
    OPENAI_API_KEY: str = ""


settings = Settings()
