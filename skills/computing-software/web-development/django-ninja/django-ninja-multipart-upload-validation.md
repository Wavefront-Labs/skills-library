---
id: computing-software.web-development.django-ninja.django-ninja-multipart-upload-validation
name: django-ninja-multipart-upload-validation
category: computing-software
field: web-development
product: django-ninja
tags: [django-ninja, file-upload, uploadedfile, form, multipart, filefield, media-root]
level: practitioner
status: docs-checked
description: "Accept a validated file plus form fields in a Django Ninja POST endpoint, store it in a FileField under MEDIA_ROOT, and serve it in development."
sources:
  - https://github.com/vitalik/django-ninja/blob/master/docs/docs/tutorial/part-6.md
  - https://github.com/vitalik/django-ninja/blob/master/docs/docs/guide/files.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: a `multipart/form-data` endpoint that takes a file and form fields, with reusable size/type validation.

## Model and settings

```python
class Attachment(models.Model):
    task = models.ForeignKey(Task, related_name="attachments", on_delete=models.CASCADE)
    file = models.FileField(upload_to="attachments/%Y/%m/")
    name = models.CharField(max_length=200)
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="attachments", on_delete=models.CASCADE
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)
```

Use `FileField`, not `ImageField` (which needs Pillow). Then run `makemigrations` and `migrate`.

```python
# settings.py
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# urls.py
urlpatterns = [...] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

`runserver` does not serve `MEDIA_ROOT` itself; `static()` returns no patterns when `DEBUG` is off, so production needs the web server or a storage service.

## Validate in the type

```python
from pathlib import Path
from typing import Annotated
from ninja import UploadedFile
from pydantic import AfterValidator, Field
from pydantic_core import PydanticCustomError

MAX_UPLOAD_SIZE = 5 * 1024 * 1024  # 5 MB
ALLOWED_EXTENSIONS = {".pdf", ".png", ".jpg", ".jpeg", ".txt", ".md"}

def check_upload(file: UploadedFile) -> UploadedFile:
    if file.size > MAX_UPLOAD_SIZE:
        raise PydanticCustomError("file_too_large", "Files can be at most 5 MB")
    if Path(file.name).suffix.lower() not in ALLOWED_EXTENSIONS:
        raise PydanticCustomError("file_type", "Only PDF, PNG, JPEG and text files are allowed")
    return file

AttachmentFile = Annotated[UploadedFile, AfterValidator(check_upload)]

class AttachmentIn(Schema):
    name: str = Field("", max_length=200)
```

A rejected file is a `422` with its own `type` and message; the error `loc` starts with `file` for the file and `form` for form fields, and errors from both are collected together.

## The endpoint

```python
@router.post("/{task_id}/attachments", response={201: AttachmentOut})
def upload_attachment(
    request,
    project_id: Path[int],
    task_id: int,
    details: Form[AttachmentIn],
    file: File[AttachmentFile],
):
    task = get_task_or_404(request.auth, project_id, task_id)
    attachment = task.attachments.create(
        file=file, name=details.name or file.name, uploaded_by=request.auth
    )
    return Status(201, attachment)
```

- `Form[Schema]` reads the schema's fields from form data (the client sends `name`, not `details`). `File[...]` reads from `request.FILES`; the body is documented as `multipart/form-data` with a file picker in the docs.
- Passing the `UploadedFile` to `create()` is enough; the `FileField` saves it under `upload_to`.
- Django keeps only the last part of the client's file name (`../../evil.pdf` is stored as `evil.pdf`); a duplicate name gets a random suffix.

## Gotchas

- Extension and `content_type` come from the client, so neither proves the contents; the check only stops e.g. an `.html` file being served as a page.
- Django has no upload size limit and the check runs after the whole file arrived; also cap the request size in the web server (e.g. nginx `client_max_body_size`).
- A `File` parameter on `PUT`/`PATCH` raises a `ConfigError` unless Ninja's compatibility middleware is added (see the File Uploads guide).
- With `curl -F`, do not set `Content-Type` yourself; curl adds the boundary.
- Media URLs need no token: anyone with the link can download. For private files use a permission-checking endpoint or signed URLs.

## Checked

2026-11-07: Confirmed against tutorial Part 6 (Storing files, Validating the upload, The upload endpoint) and the File Uploads guide (`File` parameter, `ConfigError` on PUT/PATCH, compatibility middleware). The model, settings, validator, endpoint, `loc` prefixes and gotchas all match the page text. Nothing removed.

Method: documentation only; no commands were run.
