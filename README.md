## claude-code-in-100-lines

### "Less is more"

A minimal agentic loop in under 100 lines of Python. No frameworks, no abstractions.


## How it works

Most agent frameworks hide the loop. This one exposes it:

```text
User input
    │
    ▼
LLM (with tool schemas)
    │
    ├── text response → print & done
    │
    └── tool call(s)
            │
            ▼
       execute tool
            │
            ▼
       feed result back → LLM (repeat)
```

The model sees tool schemas, decides when to call them, and the harness executes them and loops until the model returns a plain text response.

## Structure

```text
src/
  main.py        # REPL loop + builds the system prompt
  llm.py         # LLM class — message history + the tool-call loop
  tools.py       # Tool implementations + schemas
  loader.py      # Loads prompts and builds the skills index
  prompts/
    agent/       # system_prompt.md, subagent_prompt.md
    skills/      # one folder per skill, each with a SKILL.md
```

## Tools

| Tool       | Description                                            |
|------------|-------------------------------------------------------|
| `bash`     | Run a shell command, return stdout + stderr           |
| `timer`    | Sleep for N seconds                                    |
| `subagent` | Delegate a self-contained task to a fresh-context agent |

## Setup

```bash
pip install -r requirements.txt
```

Requires [Ollama](https://ollama.com) running locally with a model that supports tool use (e.g. `qwen2.5`, `llama3.1`).

To change the model, pass it when constructing `LLM` (`system`, `tools`, and `tool_schemas` are required):

```python
llm = LLM(system=SYSTEM_PROMPT, tools=TOOLS, tool_schemas=TOOL_SCHEMAS, model="qwen2.5")
```

## Run

Run from the repo root as a module (the code lives in the `src` package):

```bash
python -m src.main
```

```text
You> what files are in the current directory?
LLM> [calls bash: ls -la]
LLM> The current directory contains: main.py, llm.py, tools.py, requirements.txt ...
```

## Skills

Skills are on-demand playbooks in `src/prompts/skills/` — detailed instructions the model reads *only when a task needs them*, instead of carrying every skill's text in context on every turn (progressive disclosure). The layout follows the [Agent Skills](https://github.com/anthropics/skills) spec: one folder per skill, each with a `SKILL.md`.

At startup `loader.py` scans `src/prompts/skills/*/SKILL.md` and injects a one-line index — each skill's `description:` line plus an absolute `cat` path — into the system prompt. The model reads a skill in full with that `cat` command when a task matches; no extra tool needed, since it already has `bash`. A skill folder may include supporting files the `SKILL.md` references on demand. The subagent prompt gets the same index, so subagents use skills too.

| Skill                     | Source                                   |
|---------------------------|------------------------------------------|
| `frontend-design`         | [anthropics/skills](https://github.com/anthropics/skills) |
| `systematic-debugging`    | [obra/superpowers](https://github.com/obra/superpowers) (MIT) |
| `test-driven-development` | [obra/superpowers](https://github.com/obra/superpowers) (MIT) |
| `writing-plans`           | [obra/superpowers](https://github.com/obra/superpowers) (MIT) |
| `code-review`             | bundled                                  |
| `git-commit`              | bundled                                  |
