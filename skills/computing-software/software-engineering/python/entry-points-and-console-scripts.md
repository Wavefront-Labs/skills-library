---
id: computing-software.software-engineering.python.entry-points-and-console-scripts
name: entry-points-and-console-scripts
category: computing-software
field: software-engineering
product: python
tags: [python, python-packaging, entry-points, console-scripts, project-scripts, plugins, importlib-metadata, pipx, uv-tool]
level: practitioner
status: verified
description: "Expose Python CLIs via [project.scripts], build plugin systems with entry-point groups, discover them with importlib.metadata, and install tools with pipx/uv."
sources: ["https://packaging.python.org/en/latest/specifications/entry-points/", "https://packaging.python.org/en/latest/guides/writing-pyproject-toml/#creating-executable-scripts", "https://packaging.python.org/en/latest/guides/creating-and-discovering-plugins/", "https://docs.python.org/3/library/importlib.metadata.html#entry-points"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Entry points and console scripts

**Goal:** ship a command-line tool that works after `pip install`, and let other
packages extend yours through plugins, using the standard entry-point mechanism.

## Console scripts
```toml
[project.scripts]
mytool = "mytool.cli:main"        # creates an executable `mytool` on install

[project.gui-scripts]
mytool-gui = "mytool.gui:run"     # on Windows, no console window
```
`main` is called with no arguments; its return value becomes the exit code (`sys.exit`
semantics). Parse `sys.argv` inside (argparse/click/typer).

Also add `src/mytool/__main__.py` with `from .cli import main; raise SystemExit(main())`
so `python -m mytool` works even when the scripts dir is not on PATH.

## Installing CLIs for users
`pipx install mytool` or `uv tool install mytool` gives each tool an isolated venv and
puts the script on PATH. For local dev, `uv run mytool` or an editable install.

## Plugin systems with entry-point groups
Plugin package's pyproject:
```toml
[project.entry-points."mytool.exporters"]
csv = "mytool_csv:CsvExporter"
```
Host discovers them:
```python
from importlib.metadata import entry_points
for ep in entry_points(group="mytool.exporters"):
    exporter_cls = ep.load()     # imports lazily: only load what is used
```
- Name groups with your package prefix to avoid collisions.
- Wrap `ep.load()` in try/except and report the failing plugin by name; one broken
  plugin should not crash the host.
- pytest (`pytest11`), Flake8 and many others use exactly this mechanism.

## Gotchas
- Entry points are read from installed metadata. After editing them in pyproject, you
  must reinstall (even editable installs) to regenerate metadata.
- Two distributions defining the same script name: last installed wins silently.
- Heavy imports at module top-level of `cli.py` make `mytool --help` slow; import lazily.

## Verify
- [ ] In a fresh venv: `pip install dist/*.whl && mytool --version` works.
- [ ] `python -m mytool --help` works.
- [ ] `importlib.metadata.entry_points(group=...)` lists the test plugin.
