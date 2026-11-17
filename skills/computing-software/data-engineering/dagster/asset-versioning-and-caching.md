---
id: computing-software.data-engineering.dagster.asset-versioning-and-caching
name: asset-versioning-and-caching
category: computing-software
field: data-engineering
product: dagster
tags: [dagster, code-version, data-version, memoization, unsynced, observable-source-asset]
level: advanced
status: docs-checked
description: "Use Dagster code_version and DataVersion to skip redundant materializations, read Unsynced labels, and observe external source data."
sources:
  - https://docs.dagster.io/guides/build/assets/asset-versioning-and-caching
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Asset versioning and caching

Goal: avoid materializing assets whose result would not change.

## Concepts
- Code version: string passed as `code_version` to `@asset`.
- Data version: a `DataVersion` object. By default Dagster hashes the code version together with input data versions.
- Without an explicit `code_version`, Dagster treats every run as new code and uses the run ID as the code version, so versions change every materialization. Set `code_version="v1"`, bump it when code changes.

## What the UI shows
After bumping the version and clicking **Reload definitions**, the asset shows "Unsynced". It appears for three reasons: the code version changed, dependencies were added or removed, or a parent data version changed from a new materialization. Use the toggle beside **Materialize** and choose **Materialize unsynced**. Unsynced is not transitive: a child shows it only once its last materialization used an outdated parent.

## Custom data versions
Hashing code plus inputs can mislead: randomness gives the same data version for different outputs, and source-hash code versions change after a cosmetic refactor. Supply your own by returning an `Output` carrying a `DataVersion` alongside the value (the docs use the stringified value). Then a refactor that bumps `code_version` but yields the same data version does not mark children unsynced.

## External data
Model external inputs with `observable_source_asset`; its function returns a `DataVersion` (the docs hash a file contents). Observable source assets add an **Observe sources** button; a changed data version makes downstream assets show upstream data changed.

## Checked

2026-11-09. Pages read in full against this skill:
- https://docs.dagster.io/guides/build/assets/asset-versioning-and-caching

Confirmed: run ID as default code version, hashed data version, the three Unsynced reasons, non-transitive Unsynced, custom DataVersion via Output, observable_source_asset and the Observe sources button.
Removed or reworded: nothing; every concrete claim matched the page.

Method: documentation only; no commands were run.
