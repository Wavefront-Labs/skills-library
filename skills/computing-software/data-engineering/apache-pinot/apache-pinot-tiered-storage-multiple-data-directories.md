---
id: computing-software.data-engineering.apache-pinot.apache-pinot-tiered-storage-multiple-data-directories
name: apache-pinot-tiered-storage-multiple-data-directories
category: computing-software
field: data-engineering
product: apache-pinot
tags: [apache-pinot, tiered-storage, tierbased, tiernames, datadir, enablelocaltiermigration, segmentrelocator, tierbackendproperties, multiple-directories]
level: advanced
status: docs-checked
description: "Tiering by local disk path inside one tenant: tierBased loader, per-tier dataDir, enableLocalTierMigration and tierConfigs."
sources: ["https://github.com/pinot-contrib/pinot-docs/blob/latest/operate-pinot/separating-data-storage-by-age/using-multiple-directories.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tiered storage with multiple data directories

Keep a single tenant but give its servers several data directories, for example one backed by SSD for recent data and one backed by HDD for older data, to cut the cost of long-term history.

Server config (only the first line is required; the `tierBased` loader understands multiple directories):
```
pinot.server.instance.segment.directory.loader=tierBased
pinot.server.instance.tierConfigs.tierNames=hotTier,coldTier
pinot.server.instance.tierConfigs.hotTier.dataDir=<ssd-dir>
pinot.server.instance.tierConfigs.coldTier.dataDir=<hdd-dir>
```
`tierNames` and per-tier `dataDir` are optional but recommended on the server so they are consistent across the cluster; the table config can overwrite their values.

Controller config enables local tier migration by the SegmentRelocator:
```
controller.segmentRelocator.enableLocalTierMigration=true
```
Defaults noted on the page: `controller.segment.relocator.frequencyPeriod=3600s` and `controller.segmentRelocator.initialDelayInSeconds` a random value in [120, 300).

Table config uses `tierConfigs`, same as tiering across tenants, with each tier giving `name`, `segmentSelectorType` (`time`), `segmentAge` (for example `7d`, `15d`), `storageType` (`pinot_server`) and the same `serverTag` for every tier (the tenant's server tag, such as `base_OFFLINE`). A tier can override its directory with `tierBackendProperties.dataDir` (the path must exist on the servers); overwriting is not recommended.

Instead of moving data across tenants, segments move between data paths locally on the same servers, driven by the SegmentRelocator periodic task on the controller.

## Checked

2026-11-08. Read the whole pinot-docs using-multiple-directories page. Confirmed the loader, tier names and dataDir keys, the controller key, the relocator defaults, tierConfigs fields and the overwrite caveat. Replaced the example disk paths with placeholders and added the optional-config and table-overwrite notes.

Method: documentation only; no commands were run.
