---
id: computing-software.cloud-infrastructure-engineering.fluent-bit.dead-letter-queue
name: dead-letter-queue
category: computing-software
field: cloud-infrastructure-engineering
product: fluent-bit
tags: [fluent-bit, dead-letter-queue, storage-keep-rejected, rejected-chunks, storage-path]
level: advanced
status: docs-checked
description: "Preserve chunks Fluent Bit could not deliver by enabling the dead letter queue, and bound and inspect it."
sources: ["https://docs.fluentbit.io/manual/administration/dead-letter-queue"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Dead letter queue

The dead letter queue (DLQ) copies chunks that failed delivery into a dedicated directory instead of losing them. It needs filesystem storage: set `storage.path`, and set `storage.keep.rejected` to `on`.

Chunks are copied when:
- an output returns an unrecoverable error
- a chunk exhausts its retry attempts
- `retry_limit` is `no_retries` and a flush fails
- the scheduler cannot schedule a retry, for example under resource constraints

```yaml
service:
  storage.path: /var/log/flb-storage/
  storage.keep.rejected: on
  storage.rejected.path: rejected
  storage.rejected.limit: 500M
```

Rejected chunks go to the subdirectory named by `storage.rejected.path` under `storage.path`, here `/var/log/flb-storage/rejected/`. Once the total reaches `storage.rejected.limit` (for example `100M` or `1G`), Fluent Bit stops copying and logs a warning. Without the limit the DLQ is unbounded.

Files are named `<sanitized_tag>_<status_code>_<output_name>_<unique_id>.flb`, for example `kube_var_log_containers_test_400_http_0x7f8b4c.flb`, and hold the original records in Fluent Bit's internal format.

Files stay on disk until you remove them, so monitor the directory and apply a cleanup policy. To inspect, read the directory or enable `storage.metrics` and use the storage endpoint.

Retry behaviour that feeds the DLQ is in `computing-software.cloud-infrastructure-engineering.fluent-bit.retry-limit`.

## Checked

2026-11-03. Confirmed on the Fluent Bit Dead letter queue page and the Service section page: prerequisites, the four failure cases, location, limit behaviour and size values, file name format and example, inspection and cleanup.

Method: documentation only; no commands were run.
