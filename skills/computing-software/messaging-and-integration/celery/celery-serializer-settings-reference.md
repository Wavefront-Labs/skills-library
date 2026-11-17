---
id: computing-software.messaging-and-integration.celery.celery-serializer-settings-reference
name: celery-serializer-settings-reference
category: computing-software
field: messaging-and-integration
product: celery
tags: [celery-conf-serializers, celery, accept-content, json, pickle, result-serializer, compression, result-compression, event-serializer]
level: practitioner
status: docs-checked
description: "Reference for Celery serializer, accept_content, result_accept_content and compression settings: names, defaults and upgrade gotchas."
sources:
  - https://docs.celeryq.dev/en/stable/userguide/configuration.html
  - https://docs.celeryq.dev/en/stable/userguide/security.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Serializer, accept_content and compression settings

Goal: set the serialization and compression settings consistently and know the defaults.

## Settings
- `task_serializer`: default `"json"` (since 4.0; earlier pickle). Also `pickle`, `yaml`, `msgpack`, or any serializer registered in `kombu.serialization.registry`.
- `result_serializer`: default `json` since 4.0. The database backend honors it as of 5.7.
- `event_serializer`: default `"json"`, for event messages.
- `accept_content`: default `{'json'}` (set, list or tuple). A whitelist of content-types; any other message is discarded with an error.
- `result_accept_content`: default `None`, meaning the same as `accept_content` (added in 4.3). For the result backend.
- `task_compression`: default `None` (uncompressed). `gzip`, `bzip2` (if available), or a scheme registered in the Kombu compression registry.
- `result_compression`: default no compression; applied to stored results from 5.7.
- `task_protocol`: default 2 (since 4.0); protocols 1 and 2 are supported.

`accept_content` takes serializer names or MIME types:

```python
accept_content = ['json']
accept_content = ['application/json']
```

## Gotchas stated in the docs
- JSON supports a restricted set of types; pickle serializes almost any Python object but is inherently insecure and should be avoided whenever clients are untrusted or unauthenticated. If you add pickle or yaml to `accept_content`, make sure untrusted parties cannot access your broker.
- `accept_content` was first supported in 3.0.18; earlier versions ignore it, so run a version that supports it.
- `result_accept_content` usually matters when signed messaging is used and the result is stored unsigned in the result backend.
- `result_compression`: before 5.7 it was accepted but never used. Upgrade every worker and client to 5.7+ first and turn it on afterwards; older versions cannot read a compressed result. An unknown method now raises `ImproperlyConfigured`. It only works on backends holding arbitrary bytes (Redis, MongoDB, Cassandra, DynamoDB, Google Cloud Storage, file-system); elsewhere it is ignored with a warning and results stay uncompressed. With Redis `decode_responses=True` it is also ignored with a warning. Each compressed result records its method, so readers need not have the setting on, and results stored before it was enabled stay readable.
- For signed messages use the `auth` serializer (see the message-signing skill).

## Checked

2026-11-07. Re-read the cited page(s) (configuration, security) against this skill: parameters, defaults, setting names, classes, methods and code samples were matched to the page text. The page is long; it was read in chunks and every section relevant to this skill was covered. Code snippet and include files were not opened separately.

Removed: nothing; every claim was confirmed.

Method: documentation only; no commands were run.
