---
id: computing-software.cloud-infrastructure-engineering.jaeger.jaeger-archive-storage
name: jaeger-archive-storage
category: computing-software
field: cloud-infrastructure-engineering
product: jaeger
tags: [jaeger, traces-archive, archive-storage, jaeger-query-storage, archive-enabled]
level: practitioner
status: docs-checked
description: "Configure a second storage backend as traces_archive so selected traces outlive the primary retention."
sources:
  - https://www.jaegertracing.io/docs/2.22/storage/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: keep chosen traces long-term (for incidents or performance work).

Primary storage holds all ingested traces, needs a highly scalable backend and is typically used with a short TTL such as two weeks. Archive storage can have a much longer or infinite retention because nothing is saved to it automatically: a user must trigger a save from the Jaeger UI.

Configure it in two steps. First define a second backend (it need not be the same type as the primary):
```
jaeger_storage:
  backends:
    some_store:
      memory:
        max_traces: 100000
    another_store:
      memory:
        max_traces: 100000
```
Then reference it:
```
jaeger_query:
  storage:
    traces: some_store
    traces_archive: another_store
```

Summary: archive storage is a second named backend, referenced only by traces_archive in the query settings, and it is written only when a person saves a trace from the UI, so its retention can differ completely from the primary storage retention.

## Checked

2026-11-08: read the whole Storage Backends index page (raw markdown from the jaegertracing/documentation repo, v2/2.22). Confirmed the primary versus archive description and both config snippets. Removed unsupported claims: the archiveEnabled UI setting, that archived traces are searchable only by ID, and the Elasticsearch rollover ARCHIVE flag.

Method: documentation only; no commands were run.
