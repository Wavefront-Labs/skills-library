---
id: computing-software.web-development.django-ninja.django-ninja-nested-relations-and-query-count
name: django-ninja-nested-relations-and-query-count
category: computing-software
field: web-development
product: django-ninja
tags: [django-ninja, tutorial-relations, resolver, annotate, select-related, prefetch-related, n-plus-one]
level: practitioner
status: docs-checked
description: "Return nested related objects from ModelSchema, compute fields with resolvers and annotate, and remove N+1 queries with select_related and prefetch_related."
sources:
  - https://github.com/vitalik/django-ninja/blob/master/docs/docs/tutorial/part-2.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: accept plain ids on input, return nested objects on output, and keep list endpoints at a constant query count.

## Ids in, objects out
`ModelSchema` renders a foreign key as an id and a many-to-many as a list of ids. For output, declare the field with another schema as its type:
```python
class TaskIn(ModelSchema):
    assignee_id: int | None = None
    label_ids: list[int] = []
    class Meta:
        model = Task
        fields = ["title", "description"]

class TaskOut(ModelSchema):
    assignee: UserOut | None
    labels: list[LabelOut]
    class Meta:
        model = Task
        fields = ["id", "project", "title", "description", "created_at"]
```
Related managers (`task.labels`) are converted to lists without calling `.all()`. Declared fields come before `Meta.fields` in the output. `assignee_id` matches Django's column name, so it can go into `create()` directly.

## Creating with relations
Check client-supplied ids first (unknown user: `HttpError(400, ...)`; look labels up through `project.labels` so other projects' labels are never found). Set many-to-many after the row exists:
```python
task = Task.objects.create(project=project, **payload.dict(exclude={"label_ids"}))
task.labels.set(labels)
```

## Computed fields
A resolver is a `@staticmethod` named `resolve_<field>`:
```python
class UserOut(ModelSchema):
    display_name: str
    class Meta:
        model = User
        fields = ["id", "username"]
    @staticmethod
    def resolve_display_name(user):
        return user.get_full_name() or user.username
```
For counts, let the database compute them for the whole list:
```python
Project.objects.annotate(
    task_count=Count("tasks"),
    unassigned_task_count=Count("tasks", filter=Q(tasks__assignee=None)),
).prefetch_related("labels")
```
and declare `task_count: int` on the schema; annotations read like normal attributes. If a view returns an un-annotated object, the response fails validation with `Field required`.

`ModelSchema` never generates reverse relations; declare them yourself (`labels: list[LabelOut]` reads `project.labels`).

## Fix N+1
Each nested object costs one query per row per relation. Fetch up front:
```python
project.tasks.select_related("assignee").prefetch_related("labels").order_by("id")
```
`select_related` is for foreign keys; `prefetch_related` for many-to-many and reverse relations. To measure, wrap `ninja.testing.TestClient(api).get("/projects/1/tasks/")` in `CaptureQueriesContext(connection)` and check `len(ctx.captured_queries)`. The page reports 7 queries for three tasks without the fix and 3 with it. A single-object endpoint has no N+1 problem; optimize the lists first.

## Checked

2026-11-07: Confirmed against tutorial/part-2.md: every claim, parameter name, default, class, method, example and error string that remains was matched to the page text and its code snippets. Nothing removed.

Method: documentation only; no commands were run.
