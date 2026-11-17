---
id: computing-software.web-development.litestar.litestar-form-data-uploads
name: litestar-form-data-uploads
category: computing-software
field: web-development
product: litestar
tags: [litestar, form-data, uploads, uploadfile, multipart, urlencoded, request-max-body-size, file-upload]
level: practitioner
status: docs-checked
description: "Handle URL-encoded and multipart form data and UploadFile in Litestar, and set request_max_body_size safely."
sources: [https://docs.litestar.dev/latest/usage/requests.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Litestar form data, file uploads and body limits

Goal: accept form posts and file uploads, and bound the request size.

## Method

- URL-encoded (`application/x-www-form-urlencoded`): annotate `data` with `URLEncodedBody[T]`.
- Multipart (`multipart/form-data`): annotate `data` with `MultipartBody[T]`.
- Uploaded files become `UploadFile` (from `litestar.datastructures`); type fields accordingly. It wraps `SpooledTemporaryFile`; in a sync handler use its `read` method directly.

Single file:

```python
@post(path="/", media_type=MediaType.TEXT)
async def handle_file_upload(data: MultipartBody[UploadFile]) -> str:
    content = await data.read()
    return f"{data.filename},length: {len(content)}"
```

Structured form with known file names (any structured type):

```python
@dataclass
class FormData:
    cv: UploadFile
    diploma: UploadFile

@post(path="/")
async def h(data: MultipartBody[FormData]) -> dict[str, str]:
    cv_content = await data.cv.read()
    ...
```

Other shapes: `MultipartBody[dict[str, UploadFile]]` (iterate `data.items()`; each file has `filename`), or `MultipartBody[list[UploadFile]]` (no filenames as keys; files expose `filename`, `content_type`, `headers`). A dataclass can mix scalars and an `UploadFile` field, for example `id: int`, `name: str`, `form_input_name: UploadFile`.

Body size limit:
- `request_max_body_size` can be set on all layers; default 10MB. Over the limit returns `413 - Request Entity Too Large`.
- Set it to `None` to disable for a handler, router or controller.
- If a `Content-Length` header exceeds the limit, the body is not read; matching the real body to `Content-Length` is left to the ASGI server (e.g. uvicorn).

## Gotchas

- `request_max_body_size=None` is strongly discouraged (DoS: the whole body is read into memory); only behind a reverse proxy such as NGINX that already limits size.
- The limit is per request, so middleware and ASGI handlers reading raw ASGI events bypass it. Construct a `Request` and use `stream()` / `body()` instead.

## Verify

A body over `request_max_body_size` yields a `413` response, as the page states.

## Checked

2026-11-07. Read the full cited page(s) (usage/requests.html) and the example files they include, and confirmed the claims in this skill against that text. Nothing needed removing.

Method: documentation only; no commands were run.
