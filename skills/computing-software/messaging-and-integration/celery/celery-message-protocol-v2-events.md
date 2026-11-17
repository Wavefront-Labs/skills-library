---
id: computing-software.messaging-and-integration.celery.celery-message-protocol-v2-events
name: celery-message-protocol-v2-events
category: computing-software
field: messaging-and-integration
product: celery
tags: [celery-message-protocol, celery, protocol, task-message, headers, serialization, events, interoperability]
level: advanced
status: docs-checked
description: "Celery task message protocol v2: properties, headers and body layout, differences from v1, content types, and the event message format."
sources:
  - https://docs.celeryq.dev/en/stable/internals/protocol.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Celery message protocol v2 and event messages

Goal: publish or inspect Celery task messages from another client or language.

Version 2 is detected by the presence of a `task` header. Structure:

- properties: `correlation_id` (task id), `content_type`, `content_encoding`, optional `reply_to`.
- headers (required): `lang` ('py'), `task`, `id`, `root_id`, `parent_id`, `group`. Optional: `meth`, `shadow`, `eta` (iso8601), `expires` (iso8601), `retries`, `timelimit` (soft, hard), `argsrepr`, `kwargsrepr`, `origin` (node name), `replaced_task_nesting`, `compression` (omitted when unused; kombu compressor names such as zlib, bzip2, gzip).
- body: `(args, kwargs, embed)` where `embed` is a mapping with `callbacks`, `errbacks`, `chain` (signature lists) and `chord` (callback signature).

Minimal example publish:

```python
task_id = uuid()
args = (2, 2)
kwargs = {}
basic_publish(
    message=json.dumps((args, kwargs, None)),
    application_headers={
        'lang': 'py',
        'task': 'proj.tasks.add',
        'argsrepr': repr(args),
        'kwargsrepr': repr(kwargs),
        'origin': '@'.join([os.getpid(), socket.gethostname()])
    },
    properties={
        'correlation_id': task_id,
        'content_type': 'application/json',
        'content_encoding': 'utf-8',
    }
)
```

Changes from v1: metadata moved into headers so intermediates can decide without decoding the (possibly pickled) body; the `lang` header allows redirecting to a worker supporting the language; no `utc` flag, so times without timezone are UTC; the body holds only language-specific data (raw encoding passes the raw data as a single argument; other languages can use Thrift or protobuf); `correlation_id` replaces `task_id`; `root_id`/`parent_id` track workflows; `shadow` sets a different name for logs and monitors; `meth` is unused by Python.

Chain has a dedicated field to avoid recursion-limit problems from nested callbacks; after executing, each task pops the next signature:

```python
chain = embed['chain']
if chain:
    sig = maybe_signature(chain.pop())
    sig.apply_async(chain=chain)
```

Version 1 put all fields (`task`, `id`, `args`, `kwargs`, `retries`, `eta`, `expires`, `taskset`, `chord`, `utc`, `callbacks`, `errbacks`, `timelimit`) in the body, forcing deserialization. Content types: json `application/json`, yaml `application/x-yaml`, pickle `application/x-python-serialize`, msgpack `application/x-msgpack`.

Event messages are always JSON; since 4.0 the body is one mapping or a list of mappings. Standard fields: `type` (category-action, e.g. `task-succeeded`), `hostname`, `clock` (Lamport timestamp), `timestamp` (UNIX), `utcoffset` (hours), `pid`. The example task-succeeded message uses exchange `celeryev`, routing key `task.succeeded`, `delivery_mode` 1, plus `uuid`, `retval`, `runtime`.

## Checked

2026-11-07. Confirmed against the Celery 5.7.0 stable docs (internals/protocol.html): the settings, defaults, parameters, code and wording kept in this skill. These are the pages' own claims, not independent tests. Nothing needed removing.

Method: documentation only; no commands were run.
