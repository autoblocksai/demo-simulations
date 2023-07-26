from autoblocks.tracer import AutoblocksTracer
from simpleaichat import AIChat
from simpleaichat.utils import wikipedia_search
from simpleaichat.utils import wikipedia_search_lookup

from demo_replays.settings import env


def get_response(autoblocks: AutoblocksTracer, query: str) -> str:
    ai = AIChat(
        api_key=env.OPENAI_API_KEY,
        model="gpt-3.5-turbo",
        params=dict(temperature=0.5, max_tokens=100),
        console=False,
    )

    # Add a wrapper to the AIChat's client `post` method so that we can log
    # the requests and responses to/from OpenAI.
    original_post = ai.client.post

    def post_wrapper(*args, **kwargs):
        # Remove the headers so we don't log API keys
        filtered_kwargs = dict(kwargs)
        filtered_kwargs["headers"] = None

        # Log the request
        autoblocks.send_event("ai.intermediate.request", properties=dict(args=args, kwargs=filtered_kwargs))

        # Send the request to the original method
        response = original_post(*args, **kwargs)

        # Log the response
        autoblocks.send_event("ai.intermediate.response", properties=dict(response=response.json()))

        # Return the response
        return response

    ai.client.post = post_wrapper

    # These are tools used by the AI to respond to the user's query
    def search(q: str):
        """Search the internet."""
        autoblocks.send_event(
            "ai.tool.selected",
            properties=dict(tool_name="search"),
        )
        wiki_matches = wikipedia_search(q, n=3)
        response = dict(context=", ".join(wiki_matches), titles=wiki_matches)
        autoblocks.send_event(
            "ai.tool.response",
            properties=response,
        )
        return response

    def lookup(q: str):
        """Lookup more information about a topic."""
        autoblocks.send_event(
            "ai.tool.selected",
            properties=dict(tool_name="lookup"),
        )
        page = wikipedia_search_lookup(q, sentences=3)
        autoblocks.send_event(
            "ai.tool.response",
            properties=dict(
                page=page,
            ),
        )
        return page

    ai_response = ai(query, tools=[search, lookup])

    autoblocks.send_event(
        "ai.final.response",
        properties=dict(response=ai_response),
    )

    return ai_response["response"]
