---
id: computing-software.database-administration.vitess.vreplication-tablet-selection
name: vreplication-tablet-selection
category: computing-software
field: database-administration
product: vitess
tags: [vreplication, tablet-picker, tablet-types, cells, vstream, throttler]
level: advanced
status: docs-checked
description: "Control which source tablet a VReplication or VStream uses: cell preference, --cells, --tablet-types, CellPreference and the throttler rdonly gotcha."
sources:
  - https://vitess.io/docs/25.0/reference/vreplication/tablet_selection/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
For both VStreams (VTGate) and VReplication streams (VTTablet) the internal `TabletPicker` chooses the source (vstreamer) tablet. In VReplication the target is always the primary of the target keyspace's shard.

Cell rules: by default it looks only for healthy, serving tablets of the requested types in the local cell (or cell alias) of the calling process (the vtgate for a VStream, the target vttablet for VReplication) and picks one at random. Even with `--cells` it prefers the local cell, then cells in the same cell alias, and only then the cells listed in `--cells`. For the VStream API set `CellPreference` to `onlyspecified` with `Cells` in `VStreamFlags` to use only those cells.

Tablet types: for VReplication the candidates come from the workflow command's `--tablet-types` (default `in_order:REPLICA,PRIMARY`). Add `--tablet-types-in-preference-order` so, for example, `--tablet-types "REPLICA,PRIMARY"` uses a replica whenever possible and a primary only as fallback. For the VStream API prefer the `TabletOrder` field in `VStreamFlags`, since the `in_order` string hint will be deprecated. A VStream has no default tablet type; set `VStreamRequest.TabletType` to one type.

Warning: with the tablet throttler enabled, to use RDONLY tablets as a source for VReplication workflows or VStreams (CDC) you must run vttablet with `--throttle-tablet-types "replica,rdonly"` and also name RDONLY in the RPC call or `vtctldclient` command.

## Checked

2026-11-08. Read in full: Tablet Selection page (vitess.io docs 25.0, via the website repo markdown). Confirmed: TabletPicker role, local cell and cell alias preference order, --cells, CellPreference onlyspecified, default in_order:REPLICA,PRIMARY, --tablet-types-in-preference-order, TabletOrder, no VStream default tablet type and the throttler rdonly warning. Removed the closing sentence on typical reasons, which the page does not state.

Method: documentation only; no commands were run.
