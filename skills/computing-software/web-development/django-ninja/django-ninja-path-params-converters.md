---
id: computing-software.web-development.django-ninja.django-ninja-path-params-converters
name: django-ninja-path-params-converters
category: computing-software
field: web-development
product: django-ninja
tags: [django-ninja, path-params, path-converters, routing, type-hints, uuid]
level: intro
status: docs-checked
description: "Declare Django Ninja path parameters, get type conversion and 422 errors, and use Django path converters including path and uuid."
sources:
  - https://github.com/vitalik/django-ninja/blob/master/docs/docs/guide/path-params.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Django Ninja path parameters and converters

Goal: capture URL segments as typed view arguments.

## Declare and type
Use `{name}` in the path and a matching argument. Without an annotation the value is `str`; annotate to convert and validate:

```python
@api.get("/items/{item_id}")
def read_item(request, item_id: int):
    return {"item_id": item_id}
```

`/items/3` gives a Python `int`. A bad value returns `422` without calling the view, with an error like `"type": "int_parsing"` and `"loc": ["path", "item_id"]`.

Multiple parameters just need unique names that appear in the signature:

```python
@api.get("/events/{year}/{month}/{day}")
def events(request, year: int, month: int, day: int):
    return {"date": [year, month, day]}
```

## Django converters
Django's converters (`str`, `int`, `slug`, `uuid`, `path`) can go in the path:

```python
@api.get("/items/{int:item_id}")
def read_item(request, item_id: int):
    return {"item_id": item_id}
```

- Django rejects non-matching URLs before the view: the route does not match (a `404`, or a `422` from another matching route) rather than a validation error.
- A converter does not change the argument's Python type. An unannotated argument is still treated as `str`, so with the `int` converter it fails validation with `422`. Annotate the argument to match.
- `{uuid:...}` is rewritten internally to a `{uuidstr:...}` converter, so the view receives a plain `str`; let Pydantic or your annotation convert further.

### Slashes
The `path` converter matches the rest of the URL, slashes included:

```python
@api.get("/dir/{path:value}")
def read_path(request, value: str):
    return value
```

`/dir/some/path/with-slashes` gives `"some/path/with-slashes"`.

## Gotcha
Path parameters are always required. Giving one a default value raises an error when the app starts. Make genuinely optional values query parameters instead.

## Checked

2026-11-08: Read django-ninja docs/docs/guide/path-params.md from GitHub. Confirmed against the whole page: typed path parameters and the int_parsing 422 error, multiple parameters, Django converters and their 404 or 422 behaviour, the uuid to uuidstr rewrite, the path converter and required path parameters. Nothing removed.

Method: documentation only; no commands were run.
