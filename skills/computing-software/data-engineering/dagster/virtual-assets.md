---
id: computing-software.data-engineering.dagster.virtual-assets
name: virtual-assets
category: computing-software
field: data-engineering
product: dagster
tags: [dagster, virtual-assets, is-virtual, database-view, staleness, resolve-through-virtual]
level: advanced
status: docs-checked
description: "Mark view-like assets with is_virtual=True so Dagster looks through them for staleness, execution order and automation conditions (preview)."
sources:
  - https://docs.dagster.io/guides/build/assets/virtual-assets
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Virtual assets (preview feature)

Goal: model assets that persist no data of their own (database views, non-materialized dbt models, temporary staging tables) without treating them as independent materialization targets.

## Define
Set `is_virtual=True` on the `@asset` decorator or on `AssetSpec`.

## Behaviour changes
- Staleness (in the UI): computed through virtual assets, not at them. In `A -> B(virtual) -> C(virtual) -> D`, updating `A` does not mark `B` or `C` stale, but does mark `D` stale because its non-virtual ancestor `A` was updated since `D` was last materialized.
- Execution: when virtual assets are excluded from an execution, Dagster creates execution dependencies through them. Executing `A` and `D` together without `B` or `C` makes `A` complete before `D` begins.
- Declarative Automation: `any_deps_match()` and `all_deps_match()` evaluate against direct parents by default, so a virtual parent is evaluated itself rather than looked through. The `.resolve_through_virtual()` modifier makes conditions look through to non-virtual ancestors (documented under customizing `on_cron` and `eager`).

## Checked
2026-11-08. Confirmed against the Dagster docs page Virtual assets (raw markdown from the docs repo; the page imports a Preview notice): definition, staleness, execution and automation sections. Nothing removed.
Method: documentation only; no commands were run.
