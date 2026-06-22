from typing import Optional
import subprocess
import time

from src.llm import LLM
from src.loader import load_skills, read_prompt


def bash(command: str, timeout: Optional[int] = 10) -> str:
    """Run a shell command and return stdout + stderr.

    Args:
        command: Shell command to run
        timeout: Timeout in seconds (default 10)
    """
    try:
        r = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return f"Error: command timed out after {timeout}s"
    return r.stdout + r.stderr


def timer(seconds: int, wake_up_message: Optional[str] = None) -> str:
    """Wait for a given number of seconds, then return a completion message.

    Args:
        seconds: Seconds to wait
        wake_up_message: Optional message to return when done
    """
    time.sleep(seconds)
    msg = f"Timer of {seconds} seconds completed."
    return msg + (f" wake_up_message: {wake_up_message}" if wake_up_message else "")


def subagent(name: str, task: str) -> str:
    """Delegate a self-contained task to a fresh subagent (bash + timer, cannot nest).

    Args:
        name: Short label/role for the subagent, e.g. 'researcher'
        task: Self-contained task description; the subagent sees no prior history
    """
    child_tools = {k: v for k, v in TOOLS.items() if k != "subagent"}
    system = (
        read_prompt("subagent_prompt").replace("{{NAME}}", name).replace("{{SKILLS}}", load_skills())
    )
    return LLM(system=system, tools=child_tools).generate_response(task)


TOOLS = {"bash": bash, "timer": timer, "subagent": subagent}
