# llm_client.py
#
# One shared helper for every feature (chat + all four Part 2 ideas)
# to call the LLM through OpenRouter.
#
# All AI calls should go through this file so there is only one place
# to manage authentication, model selection, JSON responses, and tools.

import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

MODEL = "openai/gpt-oss-20b"

_client = None


def _get_client() -> OpenAI:
    global _client

    if _client is None:
        api_key = os.environ.get("OPENROUTER_API_KEY")

        if not api_key:
            raise RuntimeError(
                "OPENROUTER_API_KEY is not set in the environment."
            )

        _client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )

    return _client


def ask_gemini(
    system_prompt: str,
    user_message: str,
    max_tokens: int = 20
) -> str:
    """
    Calls the LLM through OpenRouter with a system prompt
    and user message. Returns the reply text.
    """

    response = _get_client().chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_message
            }
        ],
        max_tokens=max_tokens,
    )

    return response.choices[0].message.content


def ask_gemini_for_json(
    system_prompt: str,
    user_message: str,
    max_tokens: int = 500
) -> dict:
    """
    Calls the LLM through OpenRouter and requests a JSON response.
    """

    response = _get_client().chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_message
            }
        ],
        max_tokens=max_tokens,
        response_format={
            "type": "json_object"
        },
    )

    response_text = response.choices[0].message.content

    try:
        return json.loads(response_text)

    except json.JSONDecodeError as err:
        raise RuntimeError(
            f"Failed to parse JSON response: {response_text}"
        ) from err


def ask_gemini_with_tools(
    system_prompt: str,
    user_message: str,
    tools: list,
    tool_executor,
    max_tokens: int = 500,
    max_turns: int = 3,
) -> str:
    """
    Conversational interface with function/tool calling.

    `tools` is a list of dictionaries containing:
        name
        description
        parameters

    `tool_executor` actually runs the requested tool against
    the application's real database.

    The LLM must not guess financial numbers.
    """

    client = _get_client()

    # Convert our existing tool definitions into OpenAI/OpenRouter format.
    openrouter_tools = []

    for t in tools:
        openrouter_tools.append(
            {
                "type": "function",
                "function": {
                    "name": t["name"],
                    "description": t["description"],
                    "parameters": t["parameters"],
                },
            }
        )

    messages = [
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": user_message
        }
    ]

    for _ in range(max_turns):

        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=openrouter_tools,
            max_tokens=max_tokens,
        )

        message = response.choices[0].message

        # No tool call means the LLM has produced its final answer.
        if not message.tool_calls:
            return message.content

        # Add the assistant's tool-call message to the conversation.
        messages.append(message)

        # Execute every requested tool.
        for tool_call in message.tool_calls:

            tool_name = tool_call.function.name

            try:
                tool_args = json.loads(
                    tool_call.function.arguments
                )
            except json.JSONDecodeError as err:
                raise RuntimeError(
                    f"Invalid tool arguments: "
                    f"{tool_call.function.arguments}"
                ) from err

            # Run the REAL database operation.
            result = tool_executor(
                tool_name,
                tool_args
            )

            # Send the real result back to the LLM.
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result),
                }
            )

    raise RuntimeError(
        "Exceeded max tool-use turns without a final answer."
    )