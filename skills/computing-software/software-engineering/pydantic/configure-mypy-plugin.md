---
id: computing-software.software-engineering.pydantic.configure-mypy-plugin
name: configure-mypy-plugin
category: computing-software
field: software-engineering
product: pydantic
tags: [pydantic, pydantic-mypy-plugin, mypy, type-checking, init-typed, init-forbid-extra, static-analysis, pyproject]
level: practitioner
status: docs-checked
description: "Enable the pydantic.mypy plugin and set init_typed, init_forbid_extra and warn_required_dynamic_aliases in mypy.ini or pyproject.toml."
sources:
  - https://docs.pydantic.dev/latest/integrations/mypy/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: get Pydantic-aware type errors from mypy.

Pydantic works with mypy out of the box, and mypy already synthesizes `__init__` for models. The plugin adds Pydantic-specific checks; it is tested against the latest mypy (older versions might work but are untested).

## Enable
```ini
# mypy.ini
[mypy]
plugins = pydantic.mypy
```
```toml
# pyproject.toml
[tool.mypy]
plugins = ['pydantic.mypy']
```

## What the plugin adds
- Synthesized `__init__`: required fields without dynamically-determined aliases become required keyword args. With `validate_by_name=True` the signature uses field names, not aliases.
- Typed `model_construct` signature (no runtime validation, so static checking matters).
- Frozen models: with `frozen=True`, mutating a field is an error.
- Field `default`/`default_factory`: both together is an error, and their types must be compatible with the field.
- Untyped fields: a field without annotation is a runtime error and the plugin also reports `Untyped fields disallowed [pydantic-field]`.
- Required dynamic aliases (see `warn_required_dynamic_aliases`).

## Plugin settings
Put them in a `[pydantic-mypy]` section (`[tool.pydantic-mypy]` in pyproject). All default to `False`:
```ini
[pydantic-mypy]
init_forbid_extra = True
init_typed = True
warn_required_dynamic_aliases = True
```
- `init_typed`: Pydantic coerces (`Model(a='1')` is valid at runtime), so the plugin uses `Any` for field annotations in the synthesized `__init__` unless `init_typed` is set or strict mode is enabled on the model.
- `init_forbid_extra`: by default extra arguments are allowed and ignored, so the plugin adds `**kwargs: Any` to `__init__` unless `init_forbid_extra` is set or `extra='forbid'`.
- `warn_required_dynamic_aliases`: errors when a dynamically-determined alias or alias generator is used with `validate_by_name=False`. mypy then cannot check `__init__` calls, and falls back to `(**kwargs: Any) -> None`.

The page's strict example also sets mypy flags: `follow_imports = silent`, `warn_redundant_casts`, `warn_unused_ignores`, `disallow_any_generics`, `no_implicit_reexport`, `disallow_untyped_defs`.

## Checked

Checked 2026-11-07. Compared every claim with the Pydantic mypy integration page (integrations/mypy.md): plugin enabling snippets, the five capabilities, the `[pydantic-mypy]` / `[tool.pydantic-mypy]` section, the three settings and their False defaults, the `Untyped fields disallowed [pydantic-field]` message and the `(**kwargs: Any) -> None` fallback. All confirmed; nothing removed.

Method: documentation only; no commands were run.
