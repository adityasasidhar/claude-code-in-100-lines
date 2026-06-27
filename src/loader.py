import glob
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
AGENT_DIR = os.path.join(BASE_DIR, "prompts", "agent")
SKILLS_DIR = os.path.join(BASE_DIR, "prompts", "skills")


def read_prompt(name: str) -> str:
    """Read prompts/agent/<name>.md by stem (no extension)."""
    with open(os.path.join(AGENT_DIR, f"{name}.md")) as f:
        return f.read()


def load_skills(skills_dir: str = SKILLS_DIR) -> str:
    """Scan skills/ and return a one-line index for each skill.

    Each line includes an absolute `cat` path so the model can read the full
    skill from any working directory. Adding a skill = dropping in a folder.
    """
    # Progressive disclosure: inject only a one-line summary into the system
    # prompt. The model reads a full skill with bash("cat <path>") only when
    # the task needs it, so 6 skills cost the tokens of 6 lines, not 6 docs.
    index = []
    for path in sorted(glob.glob(os.path.join(skills_dir, "*", "SKILL.md"))):
        name = os.path.basename(os.path.dirname(path))
        description = next(
            (line.split(":", 1)[1].strip() for line in open(path) if line.startswith("description:")),
            "",
        )
        index.append(f"- `{name}`: {description}\n      read with: `cat {path}`")
    return "\n".join(index) or "(none)"
