---
id: computing-software.web-development.django-ninja.django-ninja-query-schema-grouping
name: django-ninja-query-schema-grouping
category: computing-software
field: web-development
product: django-ninja
tags: [django-ninja, query-params, query-schema, schema, pydantic]
level: practitioner
status: docs-checked
description: "Group many Django Ninja query parameters into a Schema with Query[...], make it optional, and mix it with plain parameters."
sources:
  - https://github.com/vitalik/django-ninja/blob/master/docs/docs/guide/query-params.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Group Django Ninja query parameters in a Schema

Goal: replace long query-argument lists with one validated Schema.

```python
from ninja import Query, Schema
from pydantic import Field

class Filters(Schema):
    limit: int = 100
    offset: int = 0
    query: str | None = None
    tags: list[str] = Field(None, alias="tag")

@api.get("/filter")
def filter_weapons(request, filters: Query[Filters]):
    return filters.model_dump()
```

- Every schema field is read from the query string using its own type, default and validation.
- `filters: Query[Filters]` is the preferred style; the older `filters: Filters = Query(...)` still works and means the same.
- Aliases and constraints inside a schema use Pydantic `Field(...)` (here `tags` is read from the key `tag`).

## Optional as a whole

```python
def filter_weapons(request, filters: Query[Filters | None] = None): ...
```

## Mixing with other parameters
Django Ninja merges everything before calling the view:

```python
@api.get("/filter-mixed")
def filter_mixed(request, page: int, filters: Query[Filters], sort: str = "name"):
    return dict(page=page, sort=sort, **filters.model_dump())
```

For ORM filtering built from such a schema, see Django Ninja's Filtering guide.

## Checked

2026-11-08: Read django-ninja docs/docs/guide/query-params.md from GitHub. Confirmed against the whole page: the Filters schema, Query[Filters] as the preferred style with the older default form, the optional schema form and the mixed parameters example. Changed: optional and mixed examples now use Query[Filters | None] = None and Query[Filters]; removed a claim about a default in the signature that the page does not make and a link to another skill id.

Method: documentation only; no commands were run.
