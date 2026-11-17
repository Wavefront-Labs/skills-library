---
id: computing-software.software-engineering.python.runtime-validation-with-pydantic
name: runtime-validation-with-pydantic
category: computing-software
field: software-engineering
product: python
tags: [python, pydantic, runtime-validation, pydantic-v2, basemodel, typeadapter, pydantic-settings, field-validator, strict-mode, json-schema]
level: practitioner
status: verified
description: "Validate untrusted input at Python boundaries with Pydantic v2: models, strict vs lax coercion, validators, TypeAdapter, settings from env, and performance traps."
sources: ["https://docs.pydantic.dev/latest/concepts/models/", "https://docs.pydantic.dev/latest/concepts/strict_mode/", "https://docs.pydantic.dev/latest/concepts/type_adapter/", "https://docs.pydantic.dev/latest/concepts/pydantic_settings/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Runtime validation with Pydantic v2

**Goal:** turn untrusted JSON, env vars and API payloads into typed objects at the
boundary, so the inside of the program can trust its types.

## Models
```python
from pydantic import BaseModel, Field, field_validator, ConfigDict

class Order(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    id: int
    sku: str = Field(min_length=1, max_length=64)
    qty: int = Field(gt=0)
    note: str | None = None

    @field_validator("sku")
    @classmethod
    def upper(cls, v: str) -> str:
        return v.upper()

order = Order.model_validate_json(raw_bytes)   # parse+validate in Rust core, fastest path
order.model_dump(mode="json")
```
On failure: `pydantic.ValidationError`; `e.errors()` gives structured locations for API
error responses.

## Lax vs strict
Default (lax) mode coerces `"5"` -> `5` and `"true"` -> `True`. For APIs where that
hides client bugs, use `model_config = ConfigDict(strict=True)` or per field
`Field(strict=True)`. Strict mode on JSON input still rejects `"5"` for an `int`, but accepts ISO strings for `datetime` (JSON has no datetime type); the same string is rejected from a Python dict.

## extra fields
Default `extra="ignore"` silently drops unknown keys, so typos in config go unnoticed.
Use `"forbid"` for configs and internal APIs; `"ignore"` for tolerant readers of
third-party payloads.

## Validating non-model types
```python
from pydantic import TypeAdapter
ids = TypeAdapter(list[int]).validate_python(["1", 2])
```
Create TypeAdapters once at module level; constructing them per call is slow.

## Settings from environment
```python
from pydantic_settings import BaseSettings, SettingsConfigDict
class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="APP_", env_file=".env")
    db_url: str
    debug: bool = False
settings = Settings()   # fails fast at startup if APP_DB_URL missing
```

## Gotchas
- v1 -> v2 renames: `.dict()` -> `.model_dump()`, `.parse_obj` -> `.model_validate`,
  `@validator` -> `@field_validator`; `bump-pydantic` automates much of it.
- Mutable defaults are copied per instance (safe), unlike dataclasses.
- Validate at boundaries only; passing models through hot inner loops and
  re-validating costs time.
- `model_construct()` skips validation entirely; only for trusted data.

## Verify
- [ ] Tests send a payload with a wrong type, a missing field and an extra field; each
      returns a clear 4xx with field locations.
- [ ] App refuses to start with a missing required env var.

## Checked
- pydantic 2.14.1 / pydantic-settings 2.16.1 on Python 3.14.0: ran every snippet: `model_validate_json` coerced "5" and upper-cased sku; `e.errors()` gave `greater_than`, `missing`, `extra_forbidden`, `int_parsing` with locations; frozen assignment raised; lax coerces "5" and "true"; strict and `Field(strict=True)` rejected "5" (strict JSON accepted an ISO datetime string, which corrects the old sentence); default `extra` ignores; `TypeAdapter` call; `.dict()` still works with a deprecation warning; mutable defaults copied per instance; `model_construct` skipped validation; building a TypeAdapter 2000 times took 0.038 s vs 0.001 s to validate with one; `BaseSettings` with `APP_` prefix failed on a missing `db_url` and parsed `APP_DEBUG=1` as True; `bump-pydantic` exists on PyPI (not run).
