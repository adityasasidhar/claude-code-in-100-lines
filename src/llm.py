from ollama import Client


class LLM:
    def __init__(self, system: str, tools: dict, model: str = "gemma4:31b-cloud"):
        self.model = model
        self.client = Client()
        self.messages = [{"role": "system", "content": system}] if system else []
        self.tools = tools or {}

    def generate_response(self, prompt: str) -> str:
        self.messages.append({"role": "user", "content": prompt})
        while True:
            try:
                response = self.client.chat(
                    model=self.model,
                    messages=self.messages,
                    tools=list(self.tools.values()) or None,
                )
            except Exception as e:
                return f"[LLM error: {e}] Your last request may have been too large — try a narrower one."

            self.messages.append(response.message)

            if not response.message.tool_calls:
                return response.message.content

            for call in response.message.tool_calls:
                name = call.function.name
                fn = self.tools.get(name)
                content = fn(**call.function.arguments) if fn else f"Error: unknown tool '{name}'"
                self.messages.append({"role": "tool", "tool_name": name, "content": str(content)})
