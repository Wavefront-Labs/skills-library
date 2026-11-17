---
id: computing-software.software-engineering.python.dead-code-and-complexity-metrics
name: dead-code-and-complexity-metrics
category: computing-software
field: software-engineering
product: python
tags: [python, vulture, radon, cyclomatic-complexity, dead-code, maintainability-index, python-quality]
level: practitioner
status: verified
description: "Find unused code with vulture and complex hotspots with radon or ruff's mccabe rule: whitelists for false positives, thresholds in CI, and turning reports into refactors."
sources: ["https://github.com/jendrikseipp/vulture", "https://radon.readthedocs.io/en/latest/", "https://docs.astral.sh/ruff/rules/complex-structure/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dead code and complexity metrics

**Goal:** delete code nobody calls and know which functions are too tangled to change
safely.

## Dead code with vulture
```bash
pip install vulture
vulture src/ --min-confidence 80          # 100% = certainly unused (e.g. unreachable code)
vulture src/ --make-whitelist > vulture_whitelist.py   # record intentional false positives
vulture src/ vulture_whitelist.py --min-confidence 60
```
False positives come from dynamic use: framework callbacks (Django views, pytest fixtures,
FastAPI routes), `getattr` by name, `__all__` exports, serialised field names. Whitelist them
rather than lowering confidence everywhere.

Before deleting, confirm: `git grep -n name`, search other repos that import the package,
check coverage reports (0% hit in production-like runs supports deletion).

## Complexity with radon
```bash
pip install radon
radon cc src/ -s -a -nc        # cyclomatic complexity, show score, average, only grade C or worse
radon mi src/ -s               # maintainability index per module
radon raw src/                 # LOC, comments, blank lines
radon hal src/                 # Halstead metrics
```
Grades: A (1-5) simple, B (6-10), C (11-20) complex, D/E/F (21+) refactor candidates.

## Enforce in CI with ruff (fast, already in most setups)
```toml
[tool.ruff.lint]
extend-select = ["C90", "PLR0912", "PLR0915"]   # mccabe, too many branches, too many statements
[tool.ruff.lint.mccabe]
max-complexity = 12
```
Ratchet: start the threshold at the current worst function, lower it over time; mark true
exceptions with `# noqa: C901` plus a reason.

## Using the numbers
- Combine complexity with churn: `git log --format= --name-only | sort | uniq -c | sort -rn | head`
  - complex AND frequently changed files are where refactoring pays off.
- High complexity -> extract functions, guard clauses, table-driven dispatch (see refactoring skills).
- Metrics are signals, not goals; a 40-branch state machine generated from a spec may be fine.

## Verify
- [ ] vulture runs in CI with a reviewed whitelist and no new findings.
- [ ] Complexity threshold enforced and only lowered, never raised, over time.

## Checked
- vulture, radon, ruff (current pip releases) on a scratch module: `--min-confidence 80` reported the unused import (90%) and unreachable code (100%), default run also listed 60% functions/classes/methods, `--make-whitelist` emitted whitelist lines; `radon cc -s -a` gave branchy B (6) and `-nc` printed nothing since no C or worse; `radon mi`, `raw`, `hal` ran; ruff `C901` fired with `max-complexity` set and `PLR0912` exists; the `git log ... | uniq -c` churn command ran. The A-F rank table (A 1-5 ... F 41+) matches radon's command-line docs (radon.readthedocs.io); `-n` is the documented short form of `--min`.
