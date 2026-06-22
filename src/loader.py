import glob
import os

# Anchor everything to this file so paths work regardless of the launch CWD.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
AGENT_DIR = os.path.join(BASE_DIR, "prompts", "agent")
SKILLS_DIR = os.path.join(BASE_DIR, "prompts", "skills")


def read_prompt(name: str) -> str:
    """Read prompts/agent/<name>.md by stem (no extension)."""
    with open(os.path.join(AGENT_DIR, f"{name}.md")) as f:
        return f.read()


def load_skills(skills_dir: str = SKILLS_DIR) -> str:
    """One-line index of each skills/<name>/SKILL.md, with an absolute `cat` path
    so the model can read it from any working directory. Adding a skill = dropping
    in a folder."""
    index = []
    for path in sorted(glob.glob(os.path.join(skills_dir, "*", "SKILL.md"))):
        name = os.path.basename(os.path.dirname(path))
        description = next(
            (line.split(":", 1)[1].strip() for line in open(path) if line.startswith("description:")),
            "",
        )
        index.append(f"- `{name}` — {description}\n      read with: `cat {path}`")
    return "\n".join(index) or "(none)"
