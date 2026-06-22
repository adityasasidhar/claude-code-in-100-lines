---
name: git-commit
description: Use when committing work — staging changes and writing commit messages worth reading.
---

# Git Commit

Use this when committing work.

## Before committing
- `git status` and `git diff` — know exactly what you are about to commit.
- Do not commit unrelated changes together. One logical change per commit.
- Never commit secrets, large binaries, or debug cruft. Check for them.

## The message
- **Subject line:** imperative mood, ~50 chars, no period. "Add retry to fetch", not "Added retries" or "fixes stuff".
- **Body (when the change is not trivial):** explain *why*, not *what* — the diff already shows what. Wrap at ~72 chars.
- Reference the issue/ticket if there is one.

## Rules
- Commit only when the user asks.
- If on the default branch (`main`/`master`), create a branch first.
- Stage and commit, then stop. Do not `git push` unless explicitly told to.
- Verify the commit landed: `git log --oneline -1`.
