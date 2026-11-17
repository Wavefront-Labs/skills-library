---
id: computing-software.cloud-infrastructure-engineering.zot.garbage-collection-settings
name: garbage-collection-settings
category: computing-software
field: cloud-infrastructure-engineering
product: zot
tags: [zot, garbage-collection, gc-delay, gc-interval, gc-time-window, orphan-blobs]
level: practitioner
status: docs-checked
description: "Configure Zot inline garbage collection: gc, gcDelay, gcInterval and the daily UTC gcTimeWindow, plus default behaviour for untagged manifests."
sources:
  - https://raw.githubusercontent.com/project-zot/project-zot.github.io/main/docs/articles/storage.md
  - https://raw.githubusercontent.com/project-zot/project-zot.github.io/main/docs/admin-guide/admin-configuration.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
GC is inline, so the registry needs no downtime.

Attributes (top level and `subPaths`):
- `gc`: enabled by default; `false` disables.
- `gcDelay`: default `1h`; delay before purging unreferenced blobs, so tune it for client speed and blob size. Requires `gc: true`.
- `gcInterval`: periodic interval. Requires `gc: true`.
- `gcTimeWindow`: daily UTC `HH:MM-HH:MM` window (start inclusive, end exclusive, may cross midnight, for example `22:00-06:00`) limiting when periodic sweeps start. No effect if `gcInterval` is `0` or GC is disabled. A running sweep completes. Restart required.

`gc` and `gcInterval` combinations:
- `gc` false: disabled.
- `gc` omitted: enabled, 1-hour interval.
- `gc` true, `gcInterval` omitted: 1-hour interval per the GC table.
- `gc` true, `gcInterval` 0: runs once.
- `gc` true, `gcInterval` above 0: periodic.

The docs conflict here: the attribute table says no `gcInterval` means no periodic collection. Verify behaviour on your version.

Default without `retention`: untagged manifests not referenced by indexes or artifacts are deleted after `gcDelay`. A `retention` block overrides this. If repository metadata is missing, retention decisions are skipped but the index is rewritten and eligible blobs removed.

## Checked

2026-11-04. Read against the zot storage planning article (garbage collection section and attribute table); every remaining claim found there. Removed: nothing.

Method: documentation only; no commands were run.
