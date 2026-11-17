---
id: computing-software.software-engineering.python.virtual-environments-with-venv
name: virtual-environments-with-venv
category: computing-software
field: software-engineering
product: python
tags: [python, py-environments, virtual-environments-venv, venv, pip, activate, system-site-packages]
level: practitioner
status: docs-checked
description: "Create, use and recreate virtual environments with venv: activation vs direct interpreter paths, pyvenv.cfg, system packages, options and why environments are not relocatable."
sources: ["https://docs.python.org/3/library/venv.html", "https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Virtual environments with venv

```
python3 -m venv .venv                          # isolated site-packages + a link/copy of the interpreter
.venv/bin/python -m pip install -r requirements.txt    # no activation needed: call the env's python directly
source .venv/bin/activate                      # Windows: .venv\Scripts\Activate.ps1
python -c "import sys; print(sys.prefix != sys.base_prefix)"    # True inside a venv
deactivate
```
Layout: `bin/` (`Scripts/` on Windows), `lib/pythonX.Y/site-packages` (`Lib\site-packages` on Windows), and `pyvenv.cfg` (has a `home` key and `include-system-site-packages`). Reusing an existing directory is allowed but venv may create, update or replace files in it, so use a dedicated directory.

## Options
- `--system-site-packages`: see the system's packages (rarely wanted).
- `--clear` deletes the contents of the environment directory first; `--upgrade-deps` upgrades core dependencies (pip) to the latest on PyPI (added in 3.9); `--without-pip` skips `ensurepip`; `--copies` copies the interpreter rather than symlinking (symlinks are supported on Windows but not recommended there); `--upgrade` upgrades an environment in place after the base Python was upgraded in place.
- `--prompt NAME` sets the prompt prefix.
- Since 3.13 venv creates a `.gitignore` by default.

## Conventions
- The packaging guide creates the environment in the project directory as `.venv` (`python3 -m venv .venv`).
- Never commit the env. Keep a requirements file and recreate on demand: the venv docs say to always have a simple means of recreating an environment, e.g. `pip install -r requirements.txt` with the environment's own pip.
- Use `python -m pip` to be certain which interpreter's pip runs.

## Gotchas
- Environments are inherently non-portable: installed scripts have absolute paths to the environment's interpreter in their shebang. If you move one, recreate it at the new location and delete the old one.
- Installed scripts can be run without activation by using their path; activating is not required.
- Windows PowerShell may need the execution policy set to run `Activate.ps1`: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`.
- `VIRTUAL_ENV` cannot be relied on to detect a venv (activation is optional); compare `sys.prefix` with `sys.base_prefix`.

## Verify
- [ ] After activation `python -c "import sys; print(sys.executable)"` points into `.venv`.
- [ ] `sys.prefix != sys.base_prefix` is true inside the environment.

## Checked

- 2026-11-03: checked against the CPython docs `library/venv.rst` (layout, pyvenv.cfg keys, options, 3.9 `--upgrade-deps`, 3.13 `.gitignore`, activation table, shebang non-portability warning, PowerShell execution policy, `sys.prefix != sys.base_prefix`) and the packaging.python.org guide on installing with pip and virtual environments (`.venv`, activation).
- Removed: uv commands, the PEP 668 externally-managed advice, Docker/CI PATH recipe, editor auto-detection, pyvenv.cfg `version` key, free-threaded venv note, `pip list`/`pip check` checks.

Method: documentation only; no commands were run.
