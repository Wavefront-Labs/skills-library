---
id: computing-software.data-engineering.dagster.asset-dependencies-and-code-locations
name: asset-dependencies-and-code-locations
category: computing-software
field: data-engineering
product: dagster
tags: [dagster, asset-dependencies, deps, assetspec, code-locations, source-asset]
level: practitioner
status: docs-checked
description: "Declare upstream assets with deps, link lineage across code locations, and load cross-location data with AssetSpec plus an I/O manager key."
sources:
  - https://docs.dagster.io/guides/build/assets/defining-assets-with-asset-dependencies
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Asset dependencies in Dagster

Goal: make one asset depend on another, including across code locations.

## Basic dependency
Pass the upstream asset to the `deps` parameter of the downstream `@asset`. The docs example has `sugary_cereals` selecting from the `cereals` table, and `shopping_list` selecting from `sugary_cereals`.

## Across code locations
- Assets can depend on assets in other code locations by referencing their asset key in `deps`.
- Declaring `deps` only tracks lineage. It does NOT pass the upstream data in as an input.
- Assets in different code locations cannot be materialized in the same run. To trigger the downstream asset after the upstream one materializes, use a sensor or declarative automation.

## Using the upstream data as an input
Declare the upstream asset as an `AssetSpec` in your own code location with an I/O manager key, and include the spec in `Definitions` next to the downstream asset:

`AssetSpec(...).with_io_manager_key(...)`

The docs example has `daily_sales_data` defined elsewhere and consumed by `enriched_sales_data`. `SourceAsset` was the previous way to do this and is deprecated; use `AssetSpec(...).with_io_manager_key(...)` instead.

Cross-location dependencies on partitioned assets work the same way (see partitioning assets).

## Checked

2026-11-03. Pages read in full against this skill:
- https://docs.dagster.io/guides/build/assets/defining-assets-with-asset-dependencies

Confirmed: the identifiers, settings, defaults, numbers and behaviours stated above, against the page text and its code examples.
Removed or reworded: nothing; every concrete claim matched the page.

Method: documentation only; no commands were run.
