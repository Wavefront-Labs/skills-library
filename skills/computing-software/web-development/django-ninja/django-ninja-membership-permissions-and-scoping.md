---
id: computing-software.web-development.django-ninja.django-ninja-membership-permissions-and-scoping
name: django-ninja-membership-permissions-and-scoping
category: computing-software
field: web-development
product: django-ninja
tags: [django-ninja, tutorial-permissions, roles, membership, object-level, authorization, scoped-queries]
level: advanced
status: docs-checked
description: "Authorize Django Ninja endpoints with project memberships and roles, one get_project_or_404 helper (404 vs 403), scoped querysets, and object-level comment rules."
sources:
  - https://github.com/vitalik/django-ninja/blob/master/docs/docs/tutorial/part-4.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: after authentication (`request.auth` is the `User`), decide per project and per object what a caller may do.

## Membership model
```python
class Role(models.TextChoices):
    OWNER = "owner"
    ADMIN = "admin"
    MEMBER = "member"

class Membership(models.Model):
    project = models.ForeignKey(Project, related_name="memberships", on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="memberships", on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=Role, default=Role.MEMBER)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["project", "user"], name="unique_membership")]
```
Existing projects have no members, so create memberships for them or nobody will see them. In the tutorial: member works on tasks and comments; admin also edits the project and creates labels; owner also deletes the project, adds members, and deletes anyone's comments.

## One helper for every check
```python
def get_project_or_404(user, project_id, roles=None):
    membership = get_object_or_404(
        Membership.objects.select_related("project"), project_id=project_id, user=user
    )
    if roles and membership.role not in roles:
        raise HttpError(403, f"This needs the {' or '.join(roles)} role")
    return membership.project
```
Non-members get the same `404` as for a missing project, so existence is not revealed; members lacking the role get `403` naming the role. It is a plain function (not a decorator) because the view needs the returned project anyway.

## Scope queries to the user
```python
def projects_with_counts(user):
    return (Project.objects.filter(memberships__user=user)
        .annotate(task_count=Count("tasks"), ...).prefetch_related("labels"))
```
Filter before `annotate()`; with one membership per user and project the counts stay correct. The creator becomes owner: `project.memberships.create(user=request.auth, role=Role.OWNER)`. Update uses `roles=[Role.OWNER, Role.ADMIN]`, delete `roles=[Role.OWNER]`.

Tasks: `get_task_or_404(user, project_id, task_id)` runs the project check then `get_object_or_404(project.tasks, id=task_id)`. Assignee checks should require project membership (`project.memberships.filter(user_id=...)`).

## Object-level rules (comments)
Look comments up through `task.comments` so ids from other tasks 404. Take the author from `request.auth`, never the body.
```python
if comment.author != request.auth:
    raise HttpError(403, "Only the author can edit a comment")   # edit
...
if comment.author != request.auth:
    get_project_or_404(request.auth, project_id, roles=[Role.OWNER])  # delete
```
Only the author may edit; the author or the project owner may delete. Rules about one object go in the view after loading it.

Gotcha from the page: put shared schemas like `UserOut` in a module both apps can import (here `accounts/schemas.py`) to avoid a circular import between `projects` and `tasks`.

## Checked

2026-11-07: Confirmed against tutorial Part 4 (Memberships and roles, One helper for every check, Scoping projects, Tasks and comments): the `Role` and `Membership` models, the role table, `get_project_or_404` and its 404/403 behaviour, scoped querysets, the owner on create, comment rules and the shared `UserOut` module. Nothing removed.

Method: documentation only; no commands were run.
