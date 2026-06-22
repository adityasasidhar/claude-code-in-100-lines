from src.llm import LLM
from src.loader import load_skills, read_prompt
from src.tools import TOOLS

SYSTEM_PROMPT = read_prompt("system_prompt").replace("{{SKILLS}}", load_skills())


def main():
    llm = LLM(system=SYSTEM_PROMPT, tools=TOOLS)
    while True:
        user_input = input("You> ")
        print(f"LLM> {llm.generate_response(user_input)} \n")


if __name__ == "__main__":
    main()
