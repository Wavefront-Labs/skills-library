---
id: computing-software.data-engineering.dagster.asset-factories-with-components
name: asset-factories-with-components
category: computing-software
field: data-engineering
product: dagster
tags: [dagster, asset-factory, components, dg-scaffold, defs-yaml, dg-list-defs]
level: advanced
status: docs-checked
description: "Build a Dagster asset factory as a custom component with dg scaffold, a Model class and defs.yaml, or as a plain Python function returning Definitions."
sources:
  - https://docs.dagster.io/guides/build/assets/creating-asset-factories
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Asset factories as components

Goal: generate many similar assets from configuration.

Prerequisite: a components-ready project (created with `dg`, or an existing project migrated to `dg`).

## Steps
1. Scaffold: `dg scaffold component AssetFactory`
2. Design the interface first. Create a class inheriting `dg.Model` for the per-asset attributes (for the docs ETL example), then an `AssetFactory` component with shared attributes (`access_key_id`, `secret_access_key`, set once) and an `etl_job` list attribute. The component returns a `Definitions` object containing the generated assets and the resource.
3. Instantiate it: `dg scaffold defs 'my_project.components.asset_factory.AssetFactory' asset_factory`, then fill `src/<project_name>/defs/asset_factory/defs.yaml`.
4. Inspect with `dg list defs`, or run `dg dev` for the UI.
5. Build downstream assets by referencing generated asset keys. In the docs, the key is built as `f"etl_{bucket}_{target_object}".replace(".", "_")`, so bucket `my_bucket` with `cleaned_transactions.csv` becomes `etl_my_bucket_cleaned_transactions_csv`.

## Without components
A factory is a plain function that takes configuration and returns `Definitions`.

## Checked

2026-11-03. Pages read in full against this skill:
- https://docs.dagster.io/guides/build/assets/creating-asset-factories

Confirmed: the identifiers, settings, defaults, numbers and behaviours stated above, against the page text and its code examples.
Removed or reworded: nothing; every concrete claim matched the page.

Method: documentation only; no commands were run.
