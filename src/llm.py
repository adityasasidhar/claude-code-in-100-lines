from ollama import Client


class LLM:
    def __init__(self, system: str, tools: dict, model: str = "gemma4:31b-cloud", max_steps: int = 50):
        self.model = model
        self.client = Client()
        # messages is the full conversation history. Every turn (user, assistant,
        self.messages = [{"role": "system", "content": system}] if system else []
        # tool result) gets appended here and re-sent on each call. That's how
        # the model "remembers": it sees the whole transcript every time.
        self.tools = tools or {}
        self.max_steps = max_steps  # safety cap so a stuck loop can't run forever

    def generate_response(self, prompt: str) -> str:
        self.messages.append({"role": "user", "content": prompt})

        # The agent loop: ask the model → run any tools it requests → feed
        # results back → ask again. Repeat until the model replies with plain
        # text and no tool calls. That's the whole thing every framework hides.
        for _ in range(self.max_steps):

            try:
                response = self.client.chat(
                    model=self.model,
                    messages=self.messages,
                    tools=list(self.tools.values()) or None,
                )
            except Exception as e:
                return f"[LLM error: {e}] Your last request may have been too large, try a narrower one."

            # Append before checking tool calls so the history stays consistent
            # even if a tool errors out mid-loop.
            self.messages.append(response.message)

            # No tool calls = the model has its final answer.
            if not response.message.tool_calls:
                return response.message.content

            # Run each requested tool, print it so the loop is visible to the
            # user, then feed the result back so the model can continue.
            for call in response.message.tool_calls:
                name = call.function.name
                args = call.function.arguments
                result = self.run_tool(name, args)
                preview = result[:200] + ("..." if len(result) > 200 else "")
                print(f"  ↳ {name}({args}) -> {preview}")
                self.messages.append({"role": "tool", "tool_name": name, "content": result})

        return f"[stopped after {self.max_steps} steps without a final answer]"

    def run_tool(self, name: str, args: dict) -> str:
        # Errors become text the model can read and recover from. The model sees the error and decides what to do next.
        fn = self.tools.get(name)
        if fn is None:
            return f"Error: unknown tool '{name}'"
        try:
            return str(fn(**args))
        except Exception as e:
            return f"Error running '{name}': {e}"
