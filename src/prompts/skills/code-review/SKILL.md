---
name: code-review
description: Use when asked to review code, a diff, or a PR for correctness bugs and quality issues.
---

# Code Review

Use this when asked to review code, a diff, or a PR.

## Before you start
- Get the diff: `git diff`, `git diff main...HEAD`, or `git show <sha>`.
- Read enough surrounding code to understand intent. A line is only wrong relative to what it is supposed to do.

## What to look for, in priority order
1. **Correctness** — logic errors, off-by-one, wrong operator, inverted conditions, unhandled None/null, race conditions, resource leaks.
2. **Edge cases** — empty input, zero, negative, very large input, concurrent access, partial failure.
3. **Security** — injection (shell, SQL), unvalidated input, secrets in code, unsafe deserialization.
4. **Error handling** — swallowed exceptions, missing cleanup, errors that never surface.
5. **Quality** — duplication that should be reused, dead code, misleading names, needless complexity.

## How to report
- Lead with the most serious issue. Bugs before style.
- For each finding: `file:line`, what is wrong, why it matters, and the fix.
- Distinguish "this is a bug" from "I would prefer". Do not inflate nits into blockers.
- If the diff is clean, say so plainly — do not manufacture findings.
