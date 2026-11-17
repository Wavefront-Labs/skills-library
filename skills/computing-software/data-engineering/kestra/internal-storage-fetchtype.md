---
id: computing-software.data-engineering.kestra.internal-storage-fetchtype
name: internal-storage-fetchtype
category: computing-software
field: data-engineering
product: kestra
tags: [internal-storage, fetchtype, ion, execution-context, purge, read-function]
level: practitioner
status: docs-checked
description: "Where Kestra keeps task data: execution context, internal storage, KV store; choose fetchType FETCH, FETCH_ONE, STORE or NONE and know file lifetime."
sources:
  - https://kestra.io/docs/concepts/storage
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Three places for data: the execution context (small values), internal storage (any size), the KV store (shared across a namespace).

`fetchType` on tasks that support it:

- `FETCH_ONE`: first row into the context.
- `FETCH`: all rows into the context.
- `STORE`: all rows in internal storage; a `uri` output attribute is returned.
- `NONE`: does nothing.

```yaml
- id: upload
  type: io.kestra.plugin.fs.ftp.Upload
  from: "{{ outputs.query.uri }}"
```

The execution context is one row or message with a limit "usually around 1MB", so put large payloads in internal storage. Internal storage defaults to the host filesystem, with S3, GCS and Azure Blob plugins; data uses Amazon Ion. The Serdes plugin converts Ion to and from Avro, JSON, XML, Parquet and CSV.

Lifetime: the execution context is deleted after a retention period, seven days by default (configurable). `PurgeExecution` deletes files a flow stored; `Purge` clears storage, logs and executions of earlier runs.

Caveats:

- `read()` works only on files in the same execution; a file from a previous execution returns Unauthorized.
- A namespace file read via `read()` must be in the flow's namespace.
- To parse JSON use `read()` with `fromJson()`, not `| toJson`.

## Checked

2026-11-04. Confirmed against the Kestra Storage docs page: the three storage places, the four fetchType values, the 1MB execution context limit, internal storage defaults and Ion format, the Serdes plugin, seven day retention, PurgeExecution and Purge, and the read() limits including the Unauthorized error. Nothing removed.

Method: documentation only; no commands were run.
