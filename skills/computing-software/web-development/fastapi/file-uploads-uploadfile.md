---
id: computing-software.web-development.fastapi.file-uploads-uploadfile
name: file-uploads-uploadfile
category: computing-software
field: web-development
product: fastapi
tags: [fastapi, file-upload, uploadfile, file, spooled-temporary-file, multipart]
level: practitioner
status: docs-checked
description: "Receive uploaded files in FastAPI as bytes or UploadFile, use its async methods, make files optional, and accept multiple files in one field."
sources: [https://raw.githubusercontent.com/fastapi/fastapi/master/docs/en/docs/tutorial/request-files.md]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# File uploads

Goal: read uploaded files without exhausting memory.

## Rules
- Install `python-multipart`; files arrive as form data. Import `File` and `UploadFile` from `fastapi`.
- Parameter type `bytes` (with `File()`) loads the whole content into memory: fine for small files.
- `UploadFile` is better: no `File()` default needed, a spooled file (memory up to a limit, then disk), suits large files, exposes metadata and a file-like async interface.
- Attributes: `filename`, `content_type`, `file` (a `SpooledTemporaryFile`).
- Async methods: `write(data)`, `read(size)`, `seek(offset)`, `close()`; `await myfile.seek(0)` rewinds after a read. In a plain `def` function use `myfile.file.read()`. The async methods run in a threadpool.
- Optional file: default `None`. Extra metadata: `File()` with `UploadFile`.
- Multiple files: declare a list of `bytes` or `UploadFile`.

## Limitation
Multipart encoding means no JSON `Body` fields alongside files (HTTP rule).

## Verify
Upload a file with a command-line client and print `filename` and `content_type`.

## Checked

2026-11-08: Read the Request Files page (python-multipart, bytes versus UploadFile, spooled file, attributes, async methods and threadpool, optional and multiple files, no JSON Body with files). Every claim was located; nothing removed.

Method: docs-only read of cited pages, 2026-11-08
