import os

# Memory lives in the directory the harness is run from, not inside the repo.
# That way every project the agent works in keeps its own .agent/, following
# the same pattern as a tool dropping a dotfile in your working directory.
MEMORY_DIR = os.path.join(os.getcwd(), ".agent")
MEMORY_INDEX = os.path.join(MEMORY_DIR, "MEMORY.md")  # one-line index, read on demand
MEMORY_STORE = os.path.join(MEMORY_DIR, "memory")     # one file per memory, also on demand

# The seed file gives the agent the index format so it knows how to read and
# append to it without needing any extra instructions at runtime.
_SEED = """\
# Memory

The index of long-term memory. One line per memory, each pointing at a file in `memory/`:
`- [Title](memory/<slug>.md) — one-line hook`

(empty — no memories yet)
"""


def ensure_memory() -> str:
    # Create the directory tree on first run; idempotent on every run after.
    # Returns the index path so main.py can inject it into the system prompt.
    # The agent cat's it on demand, so it costs zero tokens by default.
    os.makedirs(MEMORY_STORE, exist_ok=True)
    if not os.path.exists(MEMORY_INDEX):
        with open(MEMORY_INDEX, "w") as f:
            f.write(_SEED)
    return MEMORY_INDEX
