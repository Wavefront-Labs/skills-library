---
id: computing-software.web-development.django-ninja.django-ninja-patchdict-and-status-transitions
name: django-ninja-patchdict-and-status-transitions
category: computing-software
field: web-development
product: django-ninja
tags: [django-ninja, tutorial-workflow, patchdict, patch, http-error, state-machine, status-transition]
level: practitioner
status: docs-checked
description: "Implement PATCH partial updates with PatchDict, guard against null values, and enforce status transitions in the view with HttpError 400 and 409."
sources:
  - https://github.com/vitalik/django-ninja/blob/master/docs/docs/tutorial/part-3.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: support one-field-at-a-time updates and a status workflow that rejects invalid moves.

## PATCH with PatchDict
```python
from ninja import PatchDict

@router.patch("/{task_id}", response=TaskOut)
def update_task(request, project_id: Path[int], task_id: int, payload: PatchDict[TaskUpdate]):
    task = get_object_or_404(Task, id=task_id, project_id=project_id)
    for attr, value in payload.items():
        setattr(task, attr, value)
    ...
    task.save()
    return task
```
`PatchDict[Schema]` makes every field optional and gives the view a plain `dict` with only the keys the client sent. Field validators still run on the values sent, so a blank title is rejected on PATCH too.

## Null handling
`PatchDict` also allows `null` for every field. That is useful for a nullable column such as `due_date` (it clears it), but for NOT NULL columns it would reach `save()` and fail with an `IntegrityError`. Stop it earlier with a validator on the update schema:
```python
@field_validator("title", "description", "priority", check_fields=False)
@classmethod
def not_null(cls, value):
    if value is None:
        raise PydanticCustomError("not_null", "This field can't be null")
    return value
```
On normal requests it never fires (the type check already rejects null); it guards PATCH.

## Rules that need stored data
A validator sees only the request body, so on a partial payload it cannot know the stored `due_date`. PATCH uses the update schema, so create-only model validators do not run there. Check the rule on the object after applying changes and before saving:
```python
if task.priority == Priority.URGENT and task.due_date is None:
    raise HttpError(400, "Urgent tasks need a due date")
```
`HttpError` gives the simple `{"detail": "..."}` body rather than a list. Use validators for what the request alone decides, and view checks for anything depending on the database.

## Status transitions
Give status its own endpoint instead of PATCH. Keep the workflow as data next to the choices:
```python
ALLOWED_TRANSITIONS = {
    TaskStatus.TODO: {TaskStatus.IN_PROGRESS},
    TaskStatus.IN_PROGRESS: {TaskStatus.TODO, TaskStatus.DONE},
    TaskStatus.DONE: {TaskStatus.IN_PROGRESS},
}

class StatusIn(Schema):
    status: TaskStatus

@router.post("/{task_id}/status", response=TaskOut)
def change_status(request, project_id: Path[int], task_id: int, payload: StatusIn):
    task = get_object_or_404(Task, id=task_id, project_id=project_id)
    if payload.status not in ALLOWED_TRANSITIONS[task.status]:
        raise HttpError(409, f"Can't move a task from {task.status} to {payload.status}")
    task.status = payload.status
    task.save()
    return task
```
`StatusIn` rejects unknown statuses with a `422` enum error before the view runs. `ALLOWED_TRANSITIONS[task.status]` works with the plain string loaded from the database because a `TextChoices` member compares and hashes like its string value. `409 Conflict` marks a well-formed request that clashes with current state. Keep `status` out of the create and update schemas so new tasks start at the model default.

## Checked

2026-11-08: Read django-ninja docs/docs/tutorial/part-3.md from GitHub. Confirmed against the whole page: PatchDict behaviour and null handling, the not_null validator, view-side checks with HttpError, ALLOWED_TRANSITIONS, the status endpoint, 409 and 422 behaviour, and the TextChoices hashing note. Nothing removed.

Method: documentation only; no commands were run.
