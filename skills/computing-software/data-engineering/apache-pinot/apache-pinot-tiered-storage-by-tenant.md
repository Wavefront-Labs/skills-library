---
id: computing-software.data-engineering.apache-pinot.apache-pinot-tiered-storage-by-tenant
name: apache-pinot-tiered-storage-by-tenant
category: computing-software
field: data-engineering
product: apache-pinot
tags: [apache-pinot, tiered-storage, tierconfigs, segmentselectortype, segmentage, segmentagefield, servertag, storagetype, segmentrelocator, fixedtierselector, cold-storage]
level: advanced
status: docs-checked
description: "Moving aging segments to cheaper server tenants with tierConfigs: time selector, segmentAge, segmentAgeField, fixed selector, relocator."
sources: ["https://github.com/pinot-contrib/pinot-docs/blob/latest/operate-pinot/separating-data-storage-by-age/README.md", "https://github.com/pinot-contrib/pinot-docs/blob/latest/operate-pinot/separating-data-storage-by-age/moving-segments-across-tenants.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tiered storage across tenants

Keep recent data on fast (SSD) servers and older data on cheaper, slower (HDD) servers, trading slight latency for cost. The page notes this is not compute-storage decoupling.

Table config, using servers tagged `base_OFFLINE` plus two other tenants tagged `ssd_OFFLINE` and `hdd_OFFLINE`:
```
"tenants": { "server": "base_OFFLINE", "broker": "base_BROKER" },
"tierConfigs": [
 { "name": "ssdGroup", "segmentSelectorType": "time", "segmentAge": "7d",
   "segmentAgeField": "endTime", "storageType": "pinot_server", "serverTag": "ssd_OFFLINE" },
 { "name": "hddGroup", "segmentSelectorType": "time", "segmentAge": "15d",
   "storageType": "pinot_server", "serverTag": "hdd_OFFLINE" } ]
```
Segments older than 7 days move from `base_OFFLINE` to `ssd_OFFLINE`; older than 15 days move to `hdd_OFFLINE`.

Fields:
- `name`: unique per group.
- `segmentSelectorType`: `time` selects by segment age; `fixed` selects a list (see below).
- `segmentAge`: required for `time`; a period string such as `15d`, `24h`, `60m`.
- `segmentAgeField`: optional; `endTime` (default, the newest data), `startTime` (oldest data) or `creationTime` (when the segment was built); case-insensitive, `end_time`, `start_time`, `creation_time` also accepted.
- `storageType`: only `pinot_server`; then `serverTag` is required.

Use `creationTime` when loading historical batch data and you want transitions to begin when Pinot builds the segment; with `endTime` a newly built segment of old data can qualify for a tier immediately. Segments created before creation-time metadata was recorded are treated as already aged. `startTime` bases the move on the oldest data in each segment.

Tables without a time column cannot use time selection. Use the fixed selector with the `"*"` wildcard to match all completed (non-consuming) segments:
```
{ "segmentSelectorType": "fixed", "segmentList": ["*"], "storageType": "pinot_server", "serverTag": "<tier-tag>" }
```

The Segment Relocator periodic task on the controller moves segments as they cross each age; under the hood it runs a rebalance, so a manual rebalance has the same effect.

## Checked

2026-11-08. Read the whole pinot-docs moving-segments-across-tenants page and the section index page. Confirmed the example, field table, segmentAgeField values, creationTime advice, fixed selector wildcard and relocator behaviour. Replaced the example tag in the fixed selector with a placeholder.

Method: documentation only; no commands were run.
