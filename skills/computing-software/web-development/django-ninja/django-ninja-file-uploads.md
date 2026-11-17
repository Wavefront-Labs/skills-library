---
id: computing-software.web-development.django-ninja.django-ninja-file-uploads
name: django-ninja-file-uploads
category: computing-software
field: web-development
product: django-ninja
tags: [django-ninja, file-uploads, uploadedfile, multipart, file, put-patch]
level: practitioner
status: docs-checked
description: "Accept uploaded files in Django Ninja with UploadedFile and File, combine with Form or JSON, and fix request.FILES for PUT and PATCH."
sources:
  - https://github.com/vitalik/django-ninja/blob/master/docs/docs/guide/files.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# File uploads in Django Ninja

Goal: receive files from `request.FILES`. Any `File` parameter switches the operation to `multipart/form-data`.

```python
from ninja import NinjaAPI, UploadedFile

@api.post("/upload")
def upload(request, file: UploadedFile):
    data = file.read()
    return {"name": file.name, "len": len(data)}
```

An annotation of exactly `UploadedFile` is detected as a file automatically; marking it `File[UploadedFile]` works the same (the older `file: UploadedFile = File(...)` still works, but the annotation is preferred). `UploadedFile` is Django's class: `read(size=None)`, `multiple_chunks`, `chunks`, `name`, `size`, `content_type`, `content_type_extra`, `charset`.

## Multiple and optional
- `files: list[UploadedFile]` (set/tuple too) takes several parts sharing the field name. Several separate `UploadedFile` params each read their own field, and may mix with lists.
- Optional: `file: File[UploadedFile | None] = None`. A bare `file: UploadedFile | None = None` does not work because auto-detection needs exactly `UploadedFile`.
- Constraints go in `P(...)` (same as `Form`): `min_length`/`max_length` limit the file count, as in `images: File[list[UploadedFile], P(min_length=1, max_length=5)]`. `alias` renames the multipart field: `file: File[UploadedFile, P(alias="user-file")]`. Import `P` from `ninja`.

## With other data
Files cannot go in JSON, so send everything as multipart.

- Form style: `details: Form[UserDetails], file: File[UploadedFile]`; each schema field is its own part (the page prefers this).
- JSON style: `details: UserDetails, file: File[UploadedFile]`; `details` is one part holding a JSON string. Good for nested data.

A `Body` parameter of type Schema/list/dict is read as a JSON string; scalars (`str`, `int`, `date`, `Enum`) as plain text, same as `Form`.

## PUT and PATCH
Django populates `request.FILES` only for POST by default. Declaring a `File` on PUT/PATCH raises `ninja.errors.ConfigError` at import time. Fix by adding middleware:

```python
MIDDLEWARE = [
    # ...
    "ninja.compatibility.files.fix_request_files_middleware",
]
NINJA_FIX_REQUEST_FILES_METHODS = {"PUT", "PATCH"}  # default: PUT, PATCH, DELETE
```

## Limits
Django's `DATA_UPLOAD_MAX_MEMORY_SIZE`, `FILE_UPLOAD_MAX_MEMORY_SIZE` and `FILE_UPLOAD_PERMISSIONS` apply; Django Ninja adds no size limit of its own.

## Checked

2026-11-07: Confirmed against the File Uploads guide: `UploadedFile` auto-detection and members, lists, optional files, form versus JSON bodies, the multipart type table, the PUT/PATCH `ConfigError` and middleware, and the Django size settings. Corrected: `File(None)`, `File(..., min_length=...)`, `= File(...)` and `File()` examples now use the page forms `File[UploadedFile | None] = None`, `File[list[UploadedFile], P(min_length=1, max_length=5)]`, `File[UploadedFile, P(alias=...)]` and `file: File[UploadedFile]`; the old default form is noted as still working.

Method: documentation only; no commands were run.
