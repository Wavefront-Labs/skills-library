---
id: computing-software.web-development.django-ninja.django-ninja-first-api
name: django-ninja-first-api
category: computing-software
field: web-development
product: django-ninja
tags: [django-ninja, first-api, quickstart, install, ninjaapi, urls, django, openapi]
level: intro
status: docs-checked
description: "Install Django Ninja, create a NinjaAPI instance, add a typed GET endpoint, mount api.urls in urls.py and open the generated interactive docs."
sources:
  - https://github.com/vitalik/django-ninja/blob/master/docs/docs/quickstart/index.md
  - https://github.com/vitalik/django-ninja/blob/master/docs/docs/index.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Create a first Django Ninja API

Goal: get a working, validated, documented endpoint in an existing (or new) Django project.

## Install

```console
pip install django-ninja
```
(or `uv add django-ninja`). For a fresh project: `django-admin startproject mysite .` then `python manage.py startapp events`.

Django Ninja does not need to be in `INSTALLED_APPS`. Adding `"ninja"` only lets Django's `runserver` and `collectstatic` serve the interactive docs' assets locally instead of from a CDN.

## Create the API and mount it

```python
# mysite/api.py
from ninja import NinjaAPI

api = NinjaAPI()


@api.get("/hello")
def hello(request, name: str = "world"):
    return {"message": f"Hello, {name}!"}
```

```python
# mysite/urls.py
from django.contrib import admin
from django.urls import path

from .api import api

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),
]
```

Run `python manage.py runserver` and open `/api/hello?name=Ninja` to get `{"message": "Hello, Ninja!"}`.

What you get for free:
- `@api.get("/hello")` registers a `GET` endpoint at `/api/hello`.
- `request` is a regular Django `HttpRequest` (`request.user`, sessions and middleware work).
- `name: str = "world"` is an optional query parameter with a default.
- The returned `dict` is serialized to JSON.

## Type hints are validation

```python
@api.get("/add")
def add(request, a: int, b: int):
    return {"result": a + b}
```

`/api/add?a=2&b=3` gives `{"result": 5}` with `a` and `b` as real `int`s. `/api/add?a=2&b=three` is answered with status `422` and a `detail` list whose entry has `"loc": ["query", "b"]`, pointing at the failing parameter.

## Interactive docs

Open `/api/docs` for Swagger UI built from the same type hints; the raw OpenAPI schema is at `/api/openapi.json`.

## Gotcha

All routes under the `NinjaAPI` live below whatever prefix you give `path()` (`api/` above), so docs and schema URLs move with it.

## Checked

2026-11-07: Confirmed against quickstart/index.md, index.md: every claim, parameter name, default, class, method, example and error string that remains was matched to the page text and its code snippets. Nothing removed.

Method: documentation only; no commands were run.
