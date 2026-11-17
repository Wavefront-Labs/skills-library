---
id: computing-software.web-development.django-ninja.django-ninja-multi-app-router-layout
name: django-ninja-multi-app-router-layout
category: computing-software
field: web-development
product: django-ninja
tags: [django-ninja, tutorial-layout, add-router, path-prefix, routers, model-schema]
level: intro
status: docs-checked
description: "Lay out a multi-app Django Ninja project with one Router per app, add_router mounting, and Path[int] for router-prefix parameters."
sources:
  - https://github.com/vitalik/django-ninja/blob/master/docs/docs/tutorial/part-1.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: keep each Django app self-contained (models, schemas, router) and let one project-level module wire everything into a single `NinjaAPI`.

## Layout
Per app: models in `models.py`, schemas in `schemas.py`, endpoints in `api.py` (a `Router`). The project package holds only `api.py` (the `NinjaAPI`) and `urls.py`. Optionally add `'ninja'` to `INSTALLED_APPS` so `runserver` serves Swagger UI assets locally instead of from a CDN.

## Schemas from models
```python
from ninja import ModelSchema

class ProjectIn(ModelSchema):
    class Meta:
        model = Project
        fields = ["name", "description"]
```
A model field without a default is required in the schema; a field with `default=""` becomes optional. A foreign key listed in `fields` is serialized as the related id.

## Router per app
```python
router = Router(tags=["projects"])

@router.post("/", response={201: ProjectOut})
def create_project(request, payload: ProjectIn):
    return Status(201, Project.objects.create(**payload.dict()))

@router.delete("/{project_id}", response={204: None})
def delete_project(request, project_id: int):
    get_object_or_404(Project, id=project_id).delete()
    return Status(204, None)
```
Paths are relative; the router does not know where it is mounted. `tags=[...]` groups the app's operations in the docs. `Status(code, body)` (from `ninja`) picks one of the codes declared in `response=`; the older `(status, body)` tuples still work but are deprecated.

## Wire together
```python
api = NinjaAPI(title="TaskFlow API")
api.add_router("/projects", "projects.api.router")
api.add_router("/projects/{project_id}/tasks", "tasks.api.router")
```
`add_router()` accepts the router object or a dotted import path; the string form means the project `api.py` imports nothing from the apps, which helps avoid circular imports. In `urls.py`: `path("api/", api.urls)`.

## Prefix parameters need Path[...]
A placeholder in the router prefix is not detected automatically. Declare it as `project_id: Path[int]` (`from ninja import Path`). A plain `project_id: int` becomes a required query parameter, and the request fails with a `missing` error at `["query", "project_id"]`. Parameters in the operation's own path (`/{task_id}`) work with a plain `int`.

Take the parent id from the URL, not the body, and filter child lookups on both ids (`get_object_or_404(Task, id=task_id, project_id=project_id)`) so a task requested under the wrong project returns 404.

Mounting both routers in the project `api.py` keeps apps independent; nesting one app's router inside another (`router.add_router("/{project_id}/tasks", tasks_router)`) forces an app-to-app import and suits sub-routers of a single app.

## Checked

2026-11-07: Confirmed against tutorial/part-1.md: every claim, parameter name, default, class, method, example and error string that remains was matched to the page text and its code snippets. Nothing removed.

Method: documentation only; no commands were run.
