# claude-code-in-100-lines

### "Less is more"

> **Every agent framework hides the loop or makes it too complex. This one shows it to you — in 96 lines of Python.**
<p align="center">
  <img src="assets/loop.svg" alt="The agent loop, animated: a token circulates User to LLM to execute tool to result and back to the LLM, with a subagent spawning a fresh nested loop." width="780">
</p>


## What you'll learn

Read the source and you'll understand, concretely:

- **The agent loop** — how an LLM "uses tools": the input → model → tool-call → feed-result-back cycle that every framework wraps and hides (`llm.py`).
- **Tool dispatch** — how the model picks a tool and the harness runs it, with schemas auto-derived from plain Python docstrings, no JSON to maintain (`tools.py`).
- **Skills & progressive disclosure** — how to hand an agent deep, task-specific playbooks *without* paying for their tokens on every turn (`loader.py` + `prompts/skills/`).
- **Subagents** — how an agent spawns a fresh, isolated agent for a sub-task, and why bounding recursion matters.

If you've ever wanted to know what's *actually* happening inside Cursor, Claude Code, or an "autonomous agent," this is the whole thing with nothing hidden.

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
            ├── bash / timer ─────────────► result
            │
            └── subagent ──► fresh LLM (own history, no `subagent` tool)
                                │
                                ▼
                          runs this same loop
                                │
                                ▼
                          final message ──► result
                                │
                                ▼
                        feed result back → LLM (repeat)
```

The model sees tool schemas, decides when to call them, and the harness executes them and loops until the model returns a plain text response. One of those tools is `subagent`, which spins up a fresh `LLM` with its own message history and runs this exact loop again — a nested agent inside the agent.

## Structure

```text
src/
  main.py        # REPL loop + builds the system prompt
  llm.py         # LLM class — message history + the tool-call loop
  tools.py       # Tool implementations: bash, timer, subagent
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

Tool schemas are **not** hand-written. Ollama derives them from each function's signature and Google-style docstring, so adding a tool is just writing a function — there's no parallel JSON schema to keep in sync.

## Subagents

`subagent` lets the agent delegate a self-contained task to a brand-new `LLM` instance with its own empty message history. Use it to keep a noisy sub-task — a wide search, a long build, an exploratory dig — out of the main conversation, returning only the conclusion.

- **Fresh context.** The child sees only the task string you hand it, never the parent's history.
- **No recursion.** The child gets every tool *except* `subagent` itself (`tools.py` filters it out), so it can't spawn its own children and runaway.
- **One return value.** It runs the same tool-call loop to completion and hands back only its final message.
- **Same skills.** The subagent prompt is injected with the same skills index, so subagents follow skills just like the parent.

## Setup

```bash
pip install -r requirements.txt
```

Install ollama for linux or macos

```bash
curl -fsSL https://ollama.com/install.sh | sh

ollama pull gemma4:31b-cloud
```

Requires [Ollama](https://ollama.com) with a model that supports tool use. The default is `gemma4:31b-cloud`.

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


> ⚠️ **Not affiliated with Anthropic.** This isn't Claude Code and it doesn't call any Anthropic API. It's a from-scratch reimplementation of *how agents like Claude Code work*, running on whatever model you point Ollama at. The name is a nod to the idea, not the product.
