---
id: computing-software.cloud-infrastructure-engineering.grafana-mimir.grafana-mimir-tsdb-block-upload
name: grafana-mimir-tsdb-block-upload
category: computing-software
field: cloud-infrastructure-engineering
product: grafana-mimir
tags: [block-upload, backfill, tsdb, compactor, mimirtool]
level: advanced
status: docs-checked
description: "Documents enabling Mimir TSDB block upload for historic data, the validation checks, per-tenant enabling, Thanos limitations and cache flushing."
sources: ["https://grafana.com/docs/mimir/latest/configure/configure-tsdb-block-upload/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# TSDB block upload

Mimir can accept historic TSDB blocks from Prometheus, Cortex or other Mimir installations. Mimirtool has a `backfill` command. The feature is experimental and disabled by default.

```yaml
limits:
  compactor_block_upload_enabled: true
```

Per tenant, set `compactor_block_upload_enabled: true` in runtime overrides.

## Checks on meta.json

Rejected: non-v1 blocks; negative or inverted MinTime and MaxTime; times in the future; blocks outside retention; ranges larger than the maximum compaction range (`-compactor.block-ranges`, max default 24h); blocks crossing that boundary (for example midnight with 24h); Thanos downsampling; blocks above `compactor_block_upload_max_block_size_bytes`; blocks with Thanos external labels (some Mimir labels are allowed).

After upload, a full validation checks the blocks are well-formed. Disable with the per-tenant `compactor_block_upload_validation_enabled`, or keep index validation but skip chunk checks with `compactor_block_upload_verify_chunks`.

## Limitations

- Thanos blocks cannot be uploaded because of unsupported labels. See the Thanos/Prometheus migration guide for workarounds.
- The results cache needs flushing: samples older than 10 minutes (`-query-frontend.max-cache-freshness`) are cached in range query results, so uploaded data can make cached results wrong.

## Checked

2026-11-04. Confirmed against the Mimir page "Configure TSDB block upload": experimental and off by default, the meta.json checks, validation overrides, Thanos limitation and cache note. Nothing removed.
Method: documentation only; no commands were run.
