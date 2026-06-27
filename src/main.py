from src.llm import LLM
from src.loader import load_skills, read_prompt
from src.memory import ensure_memory
from src.tools import TOOLS

# Build the system prompt once at startup: inject the skills index and the
# memory path so the agent knows what's available without loading everything.
# Skills and memories are progressive disclosure: the agent reads them on
# demand with bash, so they cost zero tokens until actually needed.
SYSTEM_PROMPT = (
    read_prompt("system_prompt")
    .replace("{{SKILLS}}", load_skills())
    .replace("{{MEMORY}}", ensure_memory())
)


def main():
    # One LLM instance per session: it accumulates the full conversation
    # history in self.messages, so context compounds across turns.
    llm = LLM(system=SYSTEM_PROMPT, tools=TOOLS)
    while True:
        user_input = input("You> ")
        print(f"LLM> {llm.generate_response(user_input)} \n")


if __name__ == "__main__":
    main()
