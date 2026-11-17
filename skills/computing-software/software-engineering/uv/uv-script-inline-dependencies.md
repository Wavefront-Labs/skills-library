---
id: computing-software.software-engineering.uv.uv-script-inline-dependencies
name: uv-script-inline-dependencies
category: computing-software
field: software-engineering
product: uv
tags: [uv, scripts, inline-metadata, pep-723, uv-add-script, shebang, uv-run]
level: practitioner
status: docs-checked
description: "Run standalone Python scripts with uv, declare dependencies as PEP 723 inline metadata, use --with, add a shebang and select an alternative index."
sources: [https://docs.astral.sh/uv/guides/scripts/]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Scripts with inline dependencies

Goal: run a single-file script with its dependencies managed by uv, with no manual environment.

## Method

- No dependencies: `uv run example.py`; arguments follow the name. Stdin works too: `echo 'print("hello world!")' | uv run -`.
- Inside a project directory, `uv run` installs the project first. Skip that with `uv run --no-project example.py` (the flag must come before the script name).
- Per-invocation dependencies: `uv run --with rich example.py`, with constraints like `--with 'rich>12,<13'`; repeat `--with` for several. In a project these are added to the project's dependencies.
- Create a script with metadata: `uv init --script example.py --python 3.12`.
- Declare dependencies: `uv add --script example.py 'requests<3' 'rich'` writes a block at the top:

```python
# /// script
# dependencies = [
#   "requests<3",
#   "rich",
# ]
# ///
```

- Python version goes in the same block as `requires-python = ">=3.12"`. The `dependencies` field must be present even if empty. uv finds that Python, downloading it if missing.
- With inline metadata, the project's dependencies are ignored even inside a project; `--no-project` is not needed.
- Executable script: first line `#!/usr/bin/env -S uv run --script`, then `chmod +x greet` and `./greet`. A metadata block may follow after a `#` line.
- Alternative index: `uv add --index "https://example.com/simple" --script example.py 'requests<3' 'rich'` stores `[[tool.uv.index]]` with `url = ...` in the metadata.

## Gotchas

- Without a declared dependency a plain run fails with `ModuleNotFoundError`.
- Index authentication is covered by the package-index documentation, not this guide.

## Verify

A script importing `rich` fails under `uv run --no-project example.py` with `ModuleNotFoundError: No module named 'rich'`; `uv run --with rich example.py` runs it.

## Checked

2026-11-07. Every command, flag, setting, default and example was read against the full text of the cited uv documentation pages (guides/scripts). Removed or changed: nothing needed removing.

Method: documentation only; no commands were run.
