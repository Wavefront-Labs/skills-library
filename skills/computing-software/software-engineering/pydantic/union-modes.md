---
id: computing-software.software-engineering.pydantic.union-modes
name: union-modes
category: computing-software
field: software-engineering
product: pydantic
tags: [pydantic, pydantic-union-modes, smart-mode, left-to-right, union-mode, exactness, python]
level: practitioner
status: docs-checked
description: "Control how Pydantic validates untagged unions: smart mode (default) versus union_mode left_to_right, and how smart mode scores exactness and valid fields."
sources:
  - https://docs.pydantic.dev/latest/concepts/unions/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Union validation modes

Goal: predict and control which union member Pydantic picks. Unions need only **one** member valid. Three approaches exist: left to right, smart (default), and discriminated unions. The page recommends discriminated unions (more performant and predictable); for untagged unions needing order guarantees, use `union_mode='left_to_right'`.

## Left to right

Members are tried in order; the first success wins. If all fail, errors from all members are reported. Not the default because results are often surprising. Set it as a `Field` parameter:

```python
class User(BaseModel):
    id: str | int = Field(union_mode='left_to_right')
```

Order matters. With `id: int | str = Field(union_mode='left_to_right')`, `User(id='456')` gives `id=456` (an `int`), because in lax mode the numeric string is valid for `int`, tried first.

## Smart mode (default, `union_mode='smart'`)

Tries to select the best match. The algorithm may change between minor releases, so for very specific behaviour use `left_to_right` or discriminated unions.

Two metrics: number of valid fields set (models, dataclasses, TypedDicts; since v2.8.0, prioritised over exactness) and exactness. Exactness groups, best first:

1. Exact type match (e.g. `int` input to `float | int` matches `int`).
2. Would succeed in strict mode.
3. Would succeed in lax mode.

**BaseModel, dataclass, TypedDict:** members tried left to right; highest valid-fields-set count wins; ties broken by exactness; all fail returns all errors.

**Other types:** left to right; an exact match returns immediately; else the leftmost strict match; else the leftmost lax match; else all errors.

```python
class User(BaseModel):
    id: int | str | UUID
    name: str

User(id=123, name='John Doe').id    # 123
User(id='1234', name='John Doe').id # '1234' stays str (printed id='1234')
```

## Choosing

- Need guaranteed attempt order: `Field(union_mode='left_to_right')`.
- Have a tag field: use a discriminated union.
- Very specialised behaviour: a custom validator.

## Checked

Checked 2026-11-07. Re-read concepts/unions in full and compared every claim, including the smart mode algorithm and the v2.8.0 note; no changes needed.

Method: documentation only; no commands were run.
