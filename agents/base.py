import json
import logging
import uuid

from openai import OpenAI

logger = logging.getLogger(__name__)
client = OpenAI()

# In-memory conversation store keyed by session_id
conversations: dict[str, list[dict]] = {}


class Agent:
    name: str
    system_prompt: str
    tools: list[dict]

    def handle_tool_call(self, name: str, args: dict) -> tuple[str, dict | None]:
        """Process a tool call. Returns (result_message, structured_data_or_none)."""
        return ("Unknown tool", None)

    def chat(self, user_message: str, session_id: str | None = None) -> dict:
        session_id = session_id or str(uuid.uuid4())

        if session_id not in conversations:
            conversations[session_id] = [
                {"role": "system", "content": self.system_prompt},
            ]

        messages = conversations[session_id]
        messages.append({"role": "user", "content": user_message})

        tool_result = None

        while True:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                tools=self.tools,
            )

            choice = response.choices[0]
            assistant_message = choice.message
            messages.append(assistant_message.model_dump(exclude_none=True))

            if choice.finish_reason == "tool_calls" and assistant_message.tool_calls:
                for tc in assistant_message.tool_calls:
                    args = json.loads(tc.function.arguments)
                    result, data = self.handle_tool_call(tc.function.name, args)
                    if data is not None:
                        tool_result = data
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tc.id,
                        "content": result,
                    })
                continue
            break

        reply = assistant_message.content or ""
        conversations[session_id] = messages

        return {"session_id": session_id, "reply": reply, "tool_result": tool_result}

    @staticmethod
    def delete_session(session_id: str):
        conversations.pop(session_id, None)
