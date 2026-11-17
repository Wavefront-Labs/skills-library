---
id: computing-software.data-engineering.dagster.passing-data-between-assets
name: passing-data-between-assets
category: computing-software
field: data-engineering
product: dagster
tags: [dagster, io-manager, external-storage, passing-data, duckdb, deps]
level: practitioner
status: docs-checked
description: "Three ways to pass data between Dagster assets: explicit external storage with deps, I/O managers, or combining steps into one asset."
sources:
  - https://docs.dagster.io/guides/build/assets/passing-data-between-assets
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Passing data between assets

Goal: choose how downstream assets receive upstream data.

## 1. Explicit external storage (described as common and recommended)
Each asset opens its own connection (docs example: SQLite), writes or reads, and the dependency is declared with the `deps` argument. Pros: explicit and easy to understand, maximum flexibility on how and where data is stored (for example per environment). Cons: you manage connections and transactions manually and handle errors and edge cases (database down, connection closed).

## 2. I/O managers
Add upstream assets as function parameters and the I/O manager reads them; you do not need to add `deps`. The docs example installs `dagster-duckdb-pandas` and uses `DuckDBPandasIOManager` on a local file; `people()` and `birds()` write dataframes and `combined_data()` receives both as dataframes. Pros: less boilerplate, easy to swap I/O managers per environment. Cons: less flexible if you need to customize reads and writes, and the I/O manager makes some decisions for you, such as naming conventions that can be hard to override.

Warning from the docs: the local-file example works for local development, but in production each step would run in a separate environment without the same file system; consider a cloud-hosted environment.

## 3. Avoid passing data
If you modeled tasks (download, unzip, load) as assets that rely on one shared file system, combine them into one asset (`my_dataset`) that does all steps. Pros: everything defining the asset is in one place, can be faster and needs no extra compute. Cons: assumes enough disk and memory for the data, hard to reuse functions across assets, and you may not be able to swap functionality per environment (a cloud environment may not give access to the local file system).

## Checked
2026-11-08. Confirmed against the Dagster docs page Passing data between assets (raw markdown from the docs repo): all three approaches with their stated pros and cons, the production warning. Reworded the cloud-environment con to match the page's "may not". Snippets referenced by file were not read.
Method: documentation only; no commands were run.
