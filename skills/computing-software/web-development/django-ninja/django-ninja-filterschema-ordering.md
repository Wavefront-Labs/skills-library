---
id: computing-software.web-development.django-ninja.django-ninja-filterschema-ordering
name: django-ninja-filterschema-ordering
category: computing-software
field: web-development
product: django-ninja
tags: [django-ninja, filterschema, filter-lookup, ordering, query-params, django]
level: practitioner
status: docs-checked
description: "Build query-parameter filters, multi-field search and a safe Literal-restricted ordering parameter for a Django Ninja list view with FilterSchema."
sources:
  - https://github.com/vitalik/django-ninja/blob/master/docs/docs/tutorial/part-5.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: let clients filter, search and sort a list endpoint without exposing arbitrary ORM access.

## Define the filter schema

A `FilterSchema` is a `Schema` whose fields are query parameters; its `.filter()` turns the sent ones into a `Q` expression.

```python
from datetime import date
from typing import Annotated, Literal
from ninja import FilterLookup, FilterSchema

class TaskFilter(FilterSchema):
    status: Annotated[list[TaskStatus] | None, FilterLookup("status__in")] = None
    assignee: Annotated[str | None, FilterLookup("assignee__username")] = None
    label: Annotated[str | None, FilterLookup("labels__name")] = None
    due_before: Annotated[date | None, FilterLookup("due_date__lt")] = None
    search: Annotated[
        str | None, FilterLookup(["title__icontains", "description__icontains"])
    ] = None

TaskOrdering = Literal[
    "created_at", "-created_at", "due_date", "-due_date", "priority", "-priority"
]
```

- Default every field to `None`; a `None` field is skipped, so no query parameters means no filtering.
- `FilterLookup` sets the ORM lookup. Without it the field name is used (`Q(status=value)`). Public names stay short while lookups follow relations.
- A list-typed field accepts a repeated parameter: `?status=todo&status=in_progress` becomes `Q(status__in=[...])`. An unknown enum value is a `422`.
- A list of lookups (as in `search`) is combined with OR; different fields are combined with AND.

## Use it in the view

```python
@router.get("/", response=list[TaskOut])
def list_tasks(
    request,
    project_id: Path[int],
    filters: Query[TaskFilter],
    ordering: TaskOrdering = "created_at",
):
    project = get_project_or_404(request.auth, project_id)
    tasks = filters.filter(project.tasks.select_related("assignee").prefetch_related("labels"))
    return tasks.order_by(ordering, "id")
```

- `Query[TaskFilter]` reads the fields from the query string (`?status=...&search=...`, not `?filters=...`).
- Apply `filters.filter()` to a queryset already scoped to what the user may see, so filters can only narrow permissions.
- Type `ordering` as a `Literal` of allowed values. The value goes straight into `order_by()`; never pass an unchecked client string there, since it would allow sorting by any field, including related ones such as a user's password hash. `?ordering=oldest` returns a `422` with a `literal_error` item.
- Add a unique field (`"id"`) as the second `order_by` key so ties are stable, which matters once results are paginated.
- Validation errors for filter fields have `loc` containing `filters`, e.g. `["query", "filters", "status", 0]`.

## Gotchas

- `icontains` ignores case, so `search=SIGNUP` matches a description containing "signup".
- Filtering by a relation (`label=bug`) selects tasks only; a `prefetch_related` still returns every label on each task.
- On SQLite, tasks with no due date come first under `ordering=due_date`; PostgreSQL puts them last. Combine with `due_before` to exclude them.

## Checked

2026-11-07: Confirmed against tutorial/part-5.md: every claim, parameter name, default, class, method, example and error string that remains was matched to the page text and its code snippets. Nothing removed.

Method: documentation only; no commands were run.
