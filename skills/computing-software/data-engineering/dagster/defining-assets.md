---
id: computing-software.data-engineering.dagster.defining-assets
name: defining-assets
category: computing-software
field: data-engineering
product: dagster
tags: [dagster, assets, defining, decorator, asset, multi-asset, graph-asset]
level: practitioner
status: docs-checked
description: "Choose between @asset, @multi_asset, @graph_asset and @graph_multi_asset, add context, code_version and multi-part keys in Dagster."
sources:
  - https://docs.dagster.io/guides/build/assets/defining-assets
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Defining assets in Dagster

Goal: turn a Python function into an asset with the right decorator.

An asset definition has an `AssetKey` (a handle for the asset), a set of upstream asset keys, and a Python function that computes the contents from upstream dependencies and stores the results.

## Pick a decorator
- `@asset`: defines a single asset.
- `@multi_asset`: outputs multiple assets from a single operation. Useful for a single API call that updates multiple tables, or one in-memory object used to compute several assets. `my_multi_asset` is the function name, not an asset; materializing either `asset_one` or `asset_two` executes the function.
- `@graph_asset`: a single asset from multiple operations, without making each operation an asset; exposes only the final output.
- `@graph_multi_asset`: multiple assets from multiple operations.

## Context, versions, keys
- Optionally add `context` as the first parameter to receive an `AssetExecutionContext` (system information such as loggers and the run ID):

```python
import dagster as dg

@dg.asset
def context_asset(context: dg.AssetExecutionContext):
    context.log.info(f"My run ID is {context.run.run_id}")
```

- `@dg.asset(code_version="1")`: lets Dagster track assets not re-materialized since their code changed, and avoid redundant computation. The generated `AssetMaterialization` is tagged with the version, and the UI indicates when an asset's code version differs from the one used for its most recent materialization.
- Multi-part keys: pass `key_prefix` as a list of strings. The full key is the prefix prepended to the asset name (default: the decorated function's name).

Next steps listed on the page: modeling ETL pipelines with assets, asset metadata, passing data between assets, and asset factories.

## Checked
2026-11-08. Confirmed against the Dagster docs page Defining assets (raw markdown from the docs repo): asset definition parts, four decorators, context, code_version, multi-part keys. Replaced an unsupported cross-reference sentence with the page's own next-steps list. Snippets referenced by file were not read.
Method: documentation only; no commands were run.
