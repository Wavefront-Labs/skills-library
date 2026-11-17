---
id: computing-software.web-development.django-ninja.django-ninja-filter-schema
name: django-ninja-filter-schema
category: computing-software
field: web-development
product: django-ninja
tags: [django-ninja, filter-schema, filtering, filterlookup, orm, q-expression]
level: practitioner
status: docs-checked
description: "Build ORM filters from query params in Django Ninja with FilterSchema, FilterLookup, connectors, ignore_none and custom methods."
sources:
  - https://github.com/vitalik/django-ninja/blob/master/docs/docs/guide/filtering.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Filter querysets with FilterSchema

Goal: turn query params into a Django `Q` expression.

```python
from ninja import FilterSchema, NinjaAPI, Query

class BookFilterSchema(FilterSchema):
    name: str | None = None
    author: str | None = None
    created_after: datetime | None = None

@api.get("/books")
def list_books(request, filters: Query[BookFilterSchema]):
    return filters.filter(Book.objects.all())
```

Defaults: `None` fields are ignored, others become `Q(field_name=value)`, combined with AND. For the raw expression use `filters.get_filter_expression()` and combine it with your own `Q`.

## FilterLookup

```python
from typing import Annotated
from ninja import FilterLookup

name: Annotated[str | None, FilterLookup("name__icontains")] = None
search: Annotated[str | None, FilterLookup(
    ["name__icontains", "author__name__icontains", "publisher__name__icontains"]
)] = None
IContainsField = Annotated[str | None, FilterLookup("__icontains")]
```

Multiple lookups on one field are OR-ed. A lookup beginning with `__` gets the field name prepended. `Field(q=...)` still works but raises a `DeprecationWarning`.

## Connectors
- Field-level: `FilterLookup([...], expression_connector="AND")` joins one field's lookups (default `"OR"`).
- Class-level: `model_config = FilterConfigDict(expression_connector="OR")` joins different fields (default `"AND"`).
- Values: `"AND"`, `"OR"`, `"XOR"` (XOR needs Django 4.1+).

## Filtering by None
`ignore_none=False`, on `FilterLookup("tag", ignore_none=False)` or `FilterConfigDict(ignore_none=False)`, filters on `None` explicitly. Class-level only overrides field-level when set to `False`.

## Custom logic
- `def filter_<field>(self, value) -> Q`: takes precedence over `FilterLookup`.
- `def custom_expression(self) -> Q`: takes precedence over everything.

## With pagination
Filter first, then `@paginate`:

```python
@api.get("/books", response=list[BookSchema])
@paginate
def list_books(request, filters: Query[BookFilterSchema]):
    return filters.filter(Book.objects.all())
```

## Checked

2026-11-07: Confirmed against guide/filtering.md: every claim, parameter name, default, class, method, example and error string that remains was matched to the page text and its code snippets. Nothing removed.

Method: documentation only; no commands were run.
