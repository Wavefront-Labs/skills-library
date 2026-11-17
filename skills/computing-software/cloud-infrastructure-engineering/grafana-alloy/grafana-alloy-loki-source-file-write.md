---
id: computing-software.cloud-infrastructure-engineering.grafana-alloy.grafana-alloy-loki-source-file-write
name: grafana-alloy-loki-source-file-write
category: computing-software
field: cloud-infrastructure-engineering
product: grafana-alloy
tags: [lokisourcefile, lokiwrite, file-match, positions-file, tail-from-end, loki-queue-config, batch-size]
level: practitioner
status: docs-checked
description: "Read files with loki.source.file (file_match globbing, decompression, positions recovery) and ship them with loki.write batching, backoff, tenant_id and queue_config."
sources: ["https://github.com/grafana/alloy/blob/main/docs/sources/reference/components/loki/loki.source.file.md", "https://github.com/grafana/alloy/blob/main/docs/sources/reference/components/loki/loki.write.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# loki.source.file and loki.write

## Reading files
```alloy
loki.source.file "app" {
  targets    = [{ __path__ = "/var/log/app/**/*.log", job = "app" }]
  forward_to = [loki.write.default.receiver]
  file_match {
    enabled = true
  }
}
```
Without `file_match`, paths must be absolute; use `local.file_match` for globbing instead. `file_match` has `sync_period` 10s and `ignore_older_than` 0s, supports `{a,b}` alternatives and `__path_exclude__`.

- `tail_from_end` (default false) skips existing content when no stored position exists.
- `on_positions_file_error`: `restart_from_beginning` (default, may duplicate), `restart_from_end` (may lose lines) or `skip`.
- `encoding` defaults to UTF-8 and switches to UTF-16 when a BOM is present.
- `decompression` needs `enabled` and `format` (`gz`, `z`, `bz2`), set `initial_delay` so files are not read mid-compression. `tail_from_end` and `restart_from_end` are not supported when decompression is enabled.
- `file_watch` polls between `min_poll_frequency` and `max_poll_frequency`, both 250ms.

## Writing to Loki
```alloy
loki.write "default" {
  endpoint {
    url       = "https://loki.example.com/loki/api/v1/push"
    tenant_id = "team-a"
  }
}
```
Endpoint defaults: `batch_size` 1MiB, `batch_wait` 1s, `remote_timeout` 10s, `min_backoff_period` 500ms, `max_backoff_period` 5m, `max_backoff_retries` 10 (0 retries forever), `retry_on_http_429` true. Other 4xx are never retried. Without `tenant_id` no `X-Scope-OrgID` header is sent. `queue_config` defaults: `capacity` 10MiB, `block_on_overflow` true, `drain_timeout` 15s, `min_shards` 1. Multiple endpoints are fed in succession, so one slow endpoint can delay the rest.

## Checked
2026-11-04: confirmed against the loki.source.file and loki.write reference pages. Removed: the claim of one decompression format per component.
Method: documentation only; no commands were run.
