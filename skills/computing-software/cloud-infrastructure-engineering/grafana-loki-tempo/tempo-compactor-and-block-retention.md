---
id: computing-software.cloud-infrastructure-engineering.grafana-loki-tempo.tempo-compactor-and-block-retention
name: tempo-compactor-and-block-retention
category: computing-software
field: cloud-infrastructure-engineering
product: grafana-loki-tempo
tags: [tempo-retention, tempo, compaction, block-retention, compacted-block-retention, backend-scheduler]
level: practitioner
status: docs-checked
description: "Configure Tempo block retention, compaction window and compacted-block retention, and know how the backend scheduler and workers replaced the legacy compactor."
sources: ["https://grafana.com/docs/tempo/latest/operations/compaction/", "https://grafana.com/docs/tempo/latest/reference-tempo-architecture/components/compaction/", "https://grafana.com/docs/tempo/latest/configuration/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: bounded storage cost with predictable retention. Written from the current Tempo docs, where the backend scheduler and backend workers replace the legacy compactor; check which components your Tempo version runs.

How it works: Tempo stores immutable blocks in object storage. The scheduler (a singleton) creates compaction, retention and redaction jobs; stateless workers request jobs over gRPC and report back. Compaction merges small blocks, retention deletes blocks older than the retention period. A compacted block has `meta.compacted.json` instead of `meta.json` and is kept for `compacted_block_retention` so queriers with a stale blocklist can still read it.

Settings (defaults from the configuration reference):
```yaml
storage:
  trace:
    blocklist_poll: 5m
backend_worker:
  backend_scheduler_addr: backend-scheduler:9095
  compaction:
    block_retention: 336h            # default, 14 days
    compacted_block_retention: 1h    # default
    compaction_window: 1h            # default
    max_block_bytes: 107374182400    # default, 100 GB
backend_scheduler:
  provider:
    compaction:
      max_jobs_per_tenant: 1000
      min_input_blocks: 2
      max_input_blocks: 4
overrides:
  defaults:
    compaction:
      block_retention: 168h   # per-tenant; 0 (default) falls back to the global value
```
`max_compaction_objects` is deprecated in favour of `max_block_bytes`. `compaction_disabled` can pause compaction and retention per tenant. The legacy ring-based fields `max_time_per_tenant` and `compaction_cycle` are accepted but ignored.

Gotchas
- `compacted_block_retention` must be at least `2 * blocklist_poll`, and `query_frontend.search.query_backend_after` (default 15m) must also be at least `2 * blocklist_poll`.
- Compaction groups blocks only with the same window, encoding, format version and dedicated columns.
- Run one scheduler only.
- When overriding per tenant, set every field you intend; the multitenancy page warns that omitted fields can leave a `0s` value that disables retention for that tenant.

## Verify
`GET /status/backendscheduler` lists jobs, status and worker assignment. Metrics: `tempodb_blocklist_length` (high means compaction is behind), `tempodb_compaction_outstanding_blocks` (autoscaling signal), `tempodb_retention_deleted_total`, `tempo_backend_scheduler_jobs_failed_total`.

## Checked
2026-11-03. Confirmed against the Tempo compaction operations page, the compaction architecture page, the configuration reference (compaction block defaults, overrides) and the multitenancy page. Removed: the `compactor:` YAML block and compactor ring, the "retention counts from block end time" claim, the object-storage lifecycle advice, the curl metrics command and "retention 0 disables deletion" as a rule (only the multitenancy warning is kept).
Method: documentation only; no commands were run.
