---
id: computing-software.web-development.django-ninja.django-ninja-query-params-types
name: django-ninja-query-params-types
category: computing-software
field: web-development
product: django-ninja
tags: [django-ninja, query-params, query-types, list, alias, validation]
level: practitioner
status: docs-checked
description: "Read Django Ninja query parameters with defaults, bool/date conversion, repeated-key lists via Query, constraints and aliases."
sources:
  - https://github.com/vitalik/django-ninja/blob/master/docs/docs/guide/query-params.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Django Ninja query parameters: types, lists, constraints

Goal: read and validate query-string values. Any argument that is not in the path and not declared `Body`, `Form`, `File`, `Header` or `Cookie` is a query parameter.

## Required, optional, typed

```python
@api.get("/weapons")
def list_weapons(request, limit: int = 10, offset: int = 0):
    return WEAPONS[offset : offset + limit]
```

- No default means required; missing gives `422`. A default makes it optional. Unannotated means `str`.
- For optional without a real default use `q: str | None = None`.
- Types work for `str`, `int`, `float`, `bool`, `UUID`, `date`, `datetime`, enums and anything Pydantic parses.
- `bool` accepts `1/true/on/yes` as true and `0/false/off/no` as false (case insensitive); anything else (`?b=random`) is a `422`.
- `date`/`datetime` accept an ISO string (`?d=2020-01-01`) or a Unix timestamp (`?d=1577836800`).

## Lists
A bare `list` annotation is treated as a request body. To collect repeated keys (`?ids=1&ids=2&ids=3`) use `Query`:

```python
from ninja import Query

@api.get("/weapons/by-ids")
def weapons_by_ids(request, ids: Query[list[int]]):
    ...
```

Give it a default (`ids: Query[list[int]] = []`) to make the list optional.

## Constraints and aliases

```python
@api.get("/weapons/page")
def weapons_page(
    request,
    limit: Query[int, P(gt=0, le=100)] = 10,
    q: Query[str | None, P(min_length=3, max_length=50)] = None,
):
    ...

def legacy_search(request, q: Query[str, P(alias="search-term")]): ...
```

Import `P` from `ninja`. `P()` takes `gt ge lt le` for numbers, `min_length max_length pattern` for strings, plus `title description example/examples deprecated` for the OpenAPI schema. Use `alias` when the key is not a valid Python identifier or differs from the parameter name. Inside a Schema, use Pydantic `Field(...)` for constraints and aliases.

Undeclared query keys are ignored.

## Checked

2026-11-08: Read django-ninja docs/docs/guide/query-params.md from GitHub. Confirmed against the whole page: required and optional parameters, type conversion, bool and date forms, list parameters, constraints and aliases, and ignored undeclared keys. Changed: the list, constraint and alias examples now use the documented Query[...] and P(...) forms instead of Query(...) default calls, and the optional-list default is shown as = [].

Method: documentation only; no commands were run.
