"""High level helpers to run the dictionary agent."""

import json
from typing import List

from openai import OpenAI

from agent.config import settings
from agent.tools import define_contextual


client = OpenAI(api_key=settings.openai_api_key)


def run_agent(user_input: str) -> str:
    messages: List[dict] = [{"role": "user", "content": user_input}]

    tools = [
        {
            "type": "function",
            "function": {
                "name": "define_contextual",
                "description": "Get context-aware dictionary meaning of a word in a sentence",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "word": {"type": "string"},
                        "sentence": {"type": "string"},
                    },
                    "required": ["word", "sentence"],
                },
            },
        }
    ]

    response = client.chat.completions.create(
        model=settings.planner_model,
        messages=messages,
        tools=tools,
        tool_choice="auto",
    )

    if response.stop_reason == "tool_calls":
        assistant_message = response.choices[0].message

        for tool_call in assistant_message.tool_calls:
            tool_name = tool_call.function.name
            tool_args = json.loads(tool_call.function.arguments)
            tool_id = tool_call.id

            if tool_name == "define_contextual":
                result = define_contextual(
                    word=tool_args["word"],
                    sentence=tool_args.get("sentence", ""),
                )
            else:
                result = {"error": f"Unknown tool: {tool_name}"}

            messages.append(assistant_message)
            messages.append(
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "tool_result",
                            "tool_use_id": tool_id,
                            "content": json.dumps(result),
                        }
                    ],
                }
            )

        final_response = client.chat.completions.create(
            model=settings.response_model,
            messages=messages,
        )

        return final_response.choices[0].message.content or ""

    return response.choices[0].message.content or ""
