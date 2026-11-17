---
id: computing-software.software-engineering.pydantic.pipeline-api-validate-as
name: pipeline-api-validate-as
category: computing-software
field: software-engineering
product: pydantic
tags: [pydantic, pydantic-pipeline-api, experimental, validate-as, transform, annotated, validators, type-safe]
level: advanced
status: docs-checked
description: "Use the experimental Pydantic pipeline API (validate_as, transform, predicate, constraints) in Annotated types, and know when plain UserIn/UserOut models are better."
sources:
  - https://docs.pydantic.dev/latest/concepts/experimental/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Experimental pipeline API

Goal: compose parsing, constraints and transformations in `Annotated` types, more type-safely than before/after/wrap validators.

Introduced in v2.8.0, in `pydantic.experimental.pipeline`; subject to change or removal. Feedback goes to the Pydantic GitHub issues.

## Step kinds

validation (runs Pydantic validation on a type), transformation, constraint, and predicate (raises an error if it returns `False`).

## Examples from the page

```python
from typing import Annotated
from pydantic.experimental.pipeline import validate_as

class User(BaseModel):
    name: Annotated[str, validate_as(str).str_lower()]
    age: Annotated[int, validate_as(int).gt(0)]
    username: Annotated[str, validate_as(str).str_pattern(r'[a-z]+')]
    password: Annotated[str, validate_as(str).transform(str.lower).predicate(lambda x: x != 'password')]
    favorite_number: Annotated[int, (validate_as(int) | validate_as(str).str_strip().validate_as(int)).gt(0)]
    friends: Annotated[list[User], validate_as(...).len(0, 100)]
    bio: Annotated[datetime, validate_as(int).transform(lambda x: x / 1_000_000).validate_as(...)]
```

- `|` and `&` combine steps like logical OR and AND.
- `validate_as(...)` (Ellipsis) means `validate_as(<field type>)`; use `validate_as(Any)` to accept anything.
- `validate_as()` can come before or after other steps for pre- or post-processing.
- Lower-level `transform`, constraint and `predicate` methods are available.

## Mapping from validators

- BeforeValidator: `Annotated[int, validate_as(str).str_strip().validate_as(...)]`
- AfterValidator: `Annotated[int, transform(lambda x: x * 2)]` (import `transform` from the same module)
- WrapValidator: `Annotated[int, validate_as(str).str_strip().validate_as(...).transform(lambda x: x * 2)]`

## When not to use it

The page warns the all-in-one example is deliberately exhaustive; if you write this many transformations in annotations, consider `UserIn` / `UserOut` models with plain Python conversion:

```python
class UserIn(BaseModel):
    favorite_number: int | str

class UserOut(BaseModel):
    favorite_number: int

def my_api(user: UserIn) -> UserOut:
    n = user.favorite_number
    if isinstance(n, str):
        n = int(n.strip())
    return UserOut(favorite_number=n)
```

Compare verbosity, performance and ease of returning meaningful errors; do not abuse advanced patterns just because you can.

## Checked

Checked 2026-11-07. Re-read the concepts/experimental page in full and compared every claim; no changes needed.

Method: documentation only; no commands were run.
