---
id: computing-software.software-engineering.textual.textual-package-with-hatch
name: textual-package-with-hatch
category: computing-software
field: software-engineering
product: textual
tags: [textual, packaging, hatch, pypi, pyproject, entry-points, publish, pipx]
level: practitioner
status: docs-checked
description: "Package a Textual app with Hatch: scaffold with hatch new, declare dependencies and a console entry point, build, and publish to PyPI."
sources: [https://textual.textualize.io/how-to/package-with-hatch/]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Package and publish a Textual app with Hatch

Goal: let users run `pip install your-app` and then launch it by command name.

## Method

1. Scaffold: `hatch new "textual calculator"` creates `textual-calculator/` with `LICENSE.txt`, `README.md`, `pyproject.toml`, `src/textual_calculator/__about__.py`, `src/textual_calculator/__init__.py` and `tests/__init__.py`. The project directory gets a hyphen, the module directory an underscore (hyphens are illegal in imports). For existing code run `hatch new --init <YOUR PROJECT NAME>` to generate only `pyproject.toml`.
2. Put code (and `.tcss` files) in `src/<module>/`.
3. In the `[project]` table set dependencies, pinning if wanted: `dependencies = ["textual==0.47.1"]` (0.47.1 was the latest Textual when the page was written; pick the version you tested against).
4. Environment: `hatch env create` (once), then `hatch shell`. Run during development with `python -m textual_calculator.calculator`.
5. Entry point: add a function that runs the app (for example `entry_points.py`):

```python
from textual_calculator.calculator import CalculatorApp


def calculator():
    app = CalculatorApp()
    app.run()
```

Then in `pyproject.toml`:

```toml
[project.scripts]
calculator = "textual_calculator.entry_points:calculator"
```

The command name is left of `=`; right is `module:function`.
6. Install the command locally with `pip install -e .` (editable), then run `calculator`.
7. Build: `hatch build` creates a `dist` folder of archives. Hatch includes `.tcss` files; other build tools may need configuring for them.
8. Publish: create a PyPI account with 2FA, make an API token in Account Settings (the first upload needs the "Entire project" scope), then `hatch publish -u __token__ -a <YOUR API TOKEN>`. Never share or upload the token. Later, use a single-project token.
9. New release: update the version in `__about__.py`, then build and publish again.
10. Users can install with `pip install textual_calculator` or, to avoid dependency conflicts, `pipx install textual_calculator`.

## Gotchas

- The alternative to packaging is serving the app on the web with textual-serve.

## Checked
2026-11-07. Read in full: Package a Textual app with Hatch how-to. Confirmed: hatch new layout and naming, hatch new --init, dependencies pin, hatch env create / hatch shell, python -m run, entry_points.py and [project.scripts], pip install -e ., hatch build and dist, .tcss inclusion, PyPI token scopes, hatch publish command, version in __about__.py, pipx. Removed: the Verify section.
Method: documentation only; no commands were run.
