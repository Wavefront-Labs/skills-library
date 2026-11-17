---
id: computing-software.software-engineering.pydantic.configure-vscode-pylance
name: configure-vscode-pylance
category: computing-software
field: software-engineering
product: pydantic
tags: [pydantic, pydantic-vscode, vs-code, pylance, pyright, type-checking-mode, dataclass-transform, type-ignore]
level: practitioner
status: docs-checked
description: "Set up VS Code with Pylance for Pydantic and silence strict false positives from coercion using pyright ignore, Any variables, cast, and frozen class arguments."
sources:
  - https://docs.pydantic.dev/latest/integrations/visual_studio_code/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: get autocompletion and argument checking for Pydantic models in VS Code, and handle false positives from Pydantic's lenient coercion.

## Configure
1. Use the Pylance extension (installed by default with the Python extension).
2. Select the Python environment (probably a virtualenv) in which Pydantic is installed.
3. Pylance defaults to type checking `off` (autocompletion only). In User Settings, search `Type Checking Mode` (`Python > Analysis: Type Checking Mode`) and set `basic` or `strict`. You then get errors for required arguments and invalid types.
4. Optionally enable mypy: search `Mypy Enabled` (`Python > Linting: Mypy Enabled`) and check it. That includes errors from the Pydantic mypy plugin if configured.

## Why false positives happen
Pylance treats Pydantic models like pure dataclasses, so it reports strict errors, e.g. `Knight(title='Sir Lancelot', age='23')` for `age: int`, though Pydantic accepts it and converts to `23`. Passing a dict for a sub-model field (`knight={'title': 'Sir Lancelot', 'age': 23}`) is valid for Pydantic but flagged.

## Silence them selectively
- Line comment: `# type: ignore`, or `# pyright: ignore` for Pylance/pyright. Con: hides every other error on that line (misspelled or missing arguments).
- `Any` variable: `age_str: Any = '23'` then `Knight(title=..., age=age_str)`. Only that value is ignored; needs a variable per argument.
- Inline `cast`: `Knight(title='Sir Lancelot', age=cast(Any, '23'))`. The value is unchanged; checkers treat it as `Any`.

## Frozen and defaults
- Config can be set via `model_config = dict(frozen=True)` or class arguments `class Knight(BaseModel, frozen=True)`. Only the class-argument form lets Pylance detect assignments to a frozen model.
- Pylance/pyright needs `default` as a keyword to infer the field is optional: `Field(default='Sir Lancelot')` is fine, but `Field(23)` works at runtime and triggers `Argument missing for parameter "age"`. This is a dataclass-transform limitation that cannot be fixed in Pydantic.

## Mechanism
The support uses `@dataclass_transform` (PEP 681), which tells tools to treat Pydantic like dataclasses.

## Checked

Checked 2026-11-07. Compared every claim with the Visual Studio Code integration page (integrations/visual_studio_code.md): Type Checking Mode default `off` and the `basic` / `strict` options, the `Mypy Enabled` setting path, the three ways to silence strict errors, `frozen=True` as a class argument, `Field(default=...)` as keyword for pyright, and the `@dataclass_transform` / PEP 681 mechanism. All confirmed; nothing removed.

Method: documentation only; no commands were run.
