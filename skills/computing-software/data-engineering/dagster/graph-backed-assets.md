---
id: computing-software.data-engineering.dagster.graph-backed-assets
name: graph-backed-assets
category: computing-software
field: data-engineering
product: dagster
tags: [dagster, graph-asset, graph-multi-asset, can-subset, selected-output-names, ops]
level: advanced
status: docs-checked
description: "Build assets from several ops with @graph_asset, graph_multi_asset, and subsetting via can_subset and context.selected_output_names."
sources:
  - https://docs.dagster.io/guides/build/assets/graph-backed-assets
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Graph-backed assets

Goal: compute one asset from several discrete ops so runs can be re-executed at op boundaries, without persisting each intermediate value as an asset.

## Define
Use `@graph_asset`. The decorated function wires ops together. In the docs example, materializing `slack_files_table` runs `fetch_files_from_slack`, then `store_files`.

Upstream assets are inferred from the function argument names and loaded through an I/O manager (`middle_asset` depends on `upstream_asset`, `downstream_asset` on `middle_asset`).

`@graph_multi_asset` makes multiple assets from one op graph and shared upstream assets (docs: `two_assets` takes `upstream_asset`, outputs `first_asset` and `second_asset`).

## Subsetting (advanced)
By default every asset the graph produces must materialize; selecting a subset errors.

To allow it:
1. Set `can_subset=True` on the asset definition.
2. Make ops that yield graph outputs yield them optionally, checking `context.selected_output_names` (selecting only `baz_asset` yields `{"foo_2"}` from `foo`).
3. An op with a single graph output (`baz`) needs no optional output: it only runs when its asset is selected. An op whose outputs are not graph outputs (`bar`) needs nothing.

Dagster runs every op upstream of a selected output (`foo_asset` runs `foo` and `bar`; `baz_asset` runs all three).

Gotcha: if `foo` always returns both `foo_1` and `foo_2`, selecting only `baz_asset` still materializes `foo_asset`.

## Checked

2026-11-03. Pages read in full against this skill:
- https://docs.dagster.io/guides/build/assets/graph-backed-assets

Confirmed: the identifiers, settings, defaults, numbers and behaviours stated above, against the page text and its code examples.
Removed or reworded: nothing; every concrete claim matched the page.

Method: documentation only; no commands were run.
