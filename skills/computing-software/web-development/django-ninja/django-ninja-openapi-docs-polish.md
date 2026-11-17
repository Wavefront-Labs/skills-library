---
id: computing-software.web-development.django-ninja.django-ninja-openapi-docs-polish
name: django-ninja-openapi-docs-polish
category: computing-software
field: web-development
product: django-ninja
tags: [django-ninja, openapi, docs, summary, field-description, include-in-schema, deprecated]
level: practitioner
status: docs-checked
description: "Improve the generated Django Ninja OpenAPI schema with API info, summaries, docstrings, Field descriptions and examples, hidden health endpoints and deprecation."
sources:
  - https://github.com/vitalik/django-ninja/blob/master/docs/docs/tutorial/part-8.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: make the interactive docs and `/api/openapi.json` explain the API to other developers.

## API info

```python
api = NinjaAPI(title="TaskFlow API", version="1.0", description=DESCRIPTION, auth=JWTAuth())
```

These land in the `info` block of the schema. The description is rendered as Markdown (so `**Authorize**` is bold). `version` is a plain string, not parsed, but also used for the URL namespace.

## Operations

- Summary defaults to the function name in title case (`list_tasks` becomes "List Tasks"). Override with `summary="Move a task to another status"`.
- A docstring becomes the operation description (indentation removed, Markdown rendered). Use it for rules the schema cannot express, such as allowed status transitions.
- `operationId` is built from module and function name (e.g. `tasks_api_change_status`); client generators typically use it to name methods. Pass `operation_id="..."` to choose your own; it must be unique across the schema.
- `tags` come from `Router(tags=["tasks"])`.

```python
@router.post("/{task_id}/status", response=TaskOut, summary="Move a task to another status")
def change_status(request, project_id: Path[int], task_id: int, payload: StatusIn):
    """
    Allowed moves:

    - `todo` to `in_progress`
    ...
    Any other move returns **409 Conflict**.
    """
```

## Field descriptions and examples

```python
class TaskIn(TaskUpdate):
    assignee_id: int | None = Field(None, description="A member of the project", examples=[2])
    label_ids: list[int] = Field([], description="Labels of the same project", examples=[[1]])
```

- First `Field()` argument is the default. `examples` is a list of complete values, so a list field needs `[[1]]`.
- Works in a `FilterSchema` too: `search: Annotated[str | None, FilterLookup([...])] = Field(None, description="...")` shows the description beside the query parameter.

## Hide and deprecate

```python
@api.get("/health", auth=None, include_in_schema=False)
def health(request):
    return {"status": "ok"}
```

- `auth=None` lets load balancers call it without a token; `include_in_schema=False` removes it from `paths` and the docs.
- Hiding is not security: anyone who knows the URL can call it. Protect it with auth if it returns anything private.
- `deprecated=True` on an operation marks it deprecated in the schema; it keeps working. Put the replacement in the docstring (e.g. "Use `POST /api/v2/auth/token` instead.").

## Checked

2026-11-07: Confirmed against tutorial/part-8.md: every claim, parameter name, default, class, method, example and error string that remains was matched to the page text and its code snippets. Nothing removed.

Method: documentation only; no commands were run.
