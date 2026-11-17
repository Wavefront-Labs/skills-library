---
id: computing-software.web-development.django-ninja.django-ninja-absolute-file-urls-cleanup
name: django-ninja-absolute-file-urls-cleanup
category: computing-software
field: web-development
product: django-ninja
tags: [django-ninja, filefield, resolver, build-absolute-uri, file-delete, modelschema]
level: practitioner
status: docs-checked
description: "Return absolute file URLs from a Django Ninja ModelSchema resolver and delete the stored file together with its database row behind a role check."
sources:
  - https://github.com/vitalik/django-ninja/blob/master/docs/docs/tutorial/part-6.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: expose usable file URLs to API clients and avoid orphaned files on delete.

## Absolute URL in the response

A `FileField` listed in `Meta.fields` serializes as a path (`/media/attachments/2026/09/sitemap.pdf`), which does not tell a client on another host where to fetch it. Build the full URL from the request in a resolver:

```python
class AttachmentOut(ModelSchema):
    uploaded_by: UserOut
    url: str

    class Meta:
        model = Attachment
        fields = ["id", "name", "uploaded_at"]

    @staticmethod
    def resolve_url(obj, context):
        return context["request"].build_absolute_uri(obj.file.url)
```

- A resolver taking `context` receives `{"request": ..., "response_status": ...}` when the schema is used as a `response`.
- `url` is a new field that is not on the model; leave `file` out of `Meta.fields` so the relative path is not returned next to the absolute one.
- Declared fields come first in the output (`uploaded_by`, `url`, then `id`, `name`, `uploaded_at`).

## Delete the file with the row

Django never removes files from storage on its own, not even on a cascade, so delete the file explicitly:

```python
@router.delete("/{task_id}/attachments/{attachment_id}", response={204: None})
def delete_attachment(request, project_id: Path[int], task_id: int, attachment_id: int):
    task = get_task_or_404(request.auth, project_id, task_id)
    attachment = get_object_or_404(task.attachments, id=attachment_id)
    if attachment.uploaded_by != request.auth:
        get_project_or_404(request.auth, project_id, roles=[Role.OWNER, Role.ADMIN])
    attachment.file.delete(save=False)
    attachment.delete()
    return Status(204, None)
```

- Look the attachment up within the task, so an id from another task is a `404`.
- The uploader may delete their own file; anyone else needs the owner or admin role (the tutorial's helper raises a `403` for a plain member).
- `save=False` skips saving the row, which is deleted on the next line anyway.

## Gotcha

Files whose rows are removed by a cascade (deleting the whole task) stay on disk. Cleaning those up takes a periodic job or a `post_delete` signal.

## Checked

2026-11-07: Confirmed against the tutorial Part 6 page (Absolute file URLs and Deleting attachments sections): the resolver with a `context` argument (`request`, `response_status`), `build_absolute_uri()`, declared-fields-first key order, `file.delete(save=False)`, the 404 and 403 behaviour, and the cascade gotcha. Nothing removed.

Method: documentation only; no commands were run.
