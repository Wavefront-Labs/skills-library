---
id: computing-software.cloud-infrastructure-engineering.netdata.parent-retention-planning
name: parent-retention-planning
category: computing-software
field: cloud-infrastructure-engineering
product: netdata
tags: [netdata, retention-time, retention-size, disk-planning]
level: advanced
status: docs-checked
description: "Set production retention on Netdata Parents by time or by space, with the zero-means-unlimited trap and the per-metric disk estimate."
sources:
  - https://raw.githubusercontent.com/netdata/netdata/master/docs/observability-centralization-points/best-practices.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Defaults (1GB per tier) will not work for production. Pick time-based, space-based, or combined (use with caution).

Time-based (docs example), in `[db]`:

```
dbengine tier 0 retention time = 30d
dbengine tier 0 retention size = 0
dbengine tier 1 retention time = 6mo
dbengine tier 1 retention size = 0
dbengine tier 2 retention time = 5y
dbengine tier 2 retention size = 0
```

Space-based: sizes such as `dbengine tier 0 retention size = 500GB`, tier 1 `200GB`, tier 2 `100GB`, with each tier's time set to `0`.

Gotchas:
- `retention size = 0` means unlimited space, not zero.
- Size limits are soft; provision extra disk and validate in staging.
- Parents with millions of metrics: expect 100GB-1TB+ per tier.

Disk estimate: the example above uses about 3.7 MB per metric, so 1,000,000 metrics is about 3.7 TB; add 5-15% overhead for replication buffers, indexes and metadata, roughly 4 TB per million metrics.

Architecture: use multiple Parents for large estates, placed to cut bandwidth cost in multi-cloud or hybrid setups; customise retention and alerts per Parent.

## Checked

2026-11-04. Confirmed against the Netdata Observability Centralization Points best-practices page: the 1GB-per-tier default warning, the time-based, space-based and combined examples, soft size limits, the 100GB-1TB+ tip, retention size = 0 meaning unlimited, staging validation, the 3.7 MB per metric and 5-15% overhead estimate, and the multiple-Parents guidance. Removed the closing edit-config and restart line, which the page does not state.

Method: documentation only; no commands were run.
