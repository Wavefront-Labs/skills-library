---
id: computing-software.messaging-and-integration.celery.celery-task-message-serializers-compression
name: celery-task-message-serializers-compression
category: computing-software
field: messaging-and-integration
product: celery
tags: [celery, celery-task-serialization, serializer, json, pickle, msgpack, compression, accept-content]
level: practitioner
status: docs-checked
description: "Choose and configure Celery message serializers (json, pickle, yaml, msgpack) and compression (brotli, bzip2, gzip, lzma, zlib, zstd) with their precedence rules."
sources:
  - https://docs.celeryq.dev/en/stable/userguide/calling.html
  - https://docs.celeryq.dev/en/stable/userguide/security.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: pick how task messages are encoded and compressed.

## Serializers
Every message has a `content_type` header. Default is JSON; change with `task_serializer`, per task (`serializer=` on the decorator), or per call. Built in: `json`, `pickle`, `yaml`, `msgpack`; custom ones are registered with the Kombu serializer registry.
- json: cross-language, fast to decode. Only strings, Unicode, floats, Booleans, dicts, lists (no Decimals or dates). Binary uses Base64, 34% larger. Dict keys are coerced to strings, so `loads(dumps(x)) != x` for non-string keys. Warning: complex canvas workflows can drastically inflate JSON message size because of recursive references; pickle is not vulnerable to this.
- pickle: Python only; supports all built-in types (except class instances), smaller binary messages, slightly faster. It is inherently insecure and should be avoided whenever clients are untrusted or unauthenticated (see the security guide); the `auth` serializer signs messages.
- yaml: like json but more types (dates, recursive references); slower libraries. `pip install celery[yaml]`.
- msgpack: binary, closer to JSON in features, compresses better and is faster. `pip install celery[msgpack]`.

To use a non-JSON format add its content type to `accept_content`; by default only JSON is accepted and other content types are rejected.

Precedence when sending: 1) the `serializer` execution option, 2) the `Task.serializer` attribute, 3) the `task_serializer` setting.
```python
add.apply_async((10, 10), serializer='json')
```

## Compression
Built-in schemes: `brotli` (`pip install celery[brotli]`), `bzip2` (smaller than gzip but slower; needs Python built with bz2), `gzip` (small memory footprint), `lzma` (good ratio, fast, more memory; `pip install celery[lzma]` backport), `zlib`, `zstd` (`pip install celery[zstd]`). If `import bz2` (or gzip, lzma, zlib) raises `ImportError`, recompile Python with that support. Register custom schemes in the kombu compression registry.

Precedence: 1) `compression` execution option, 2) `Task.compression` attribute, 3) `task_compression` setting.
```python
add.apply_async((2, 2), compression='zlib')
```

## Checked

2026-11-07. Re-read the cited page(s) (calling, security) against this skill: parameters, defaults, setting names, classes, methods and code samples were matched to the page text. Code snippet and include files were not opened separately.

Changed: replaced an unsupported pickle claim with the security page wording and added the security page to sources.

Method: documentation only; no commands were run.
