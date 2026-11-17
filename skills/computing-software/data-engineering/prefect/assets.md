---
id: computing-software.data-engineering.prefect.assets
name: assets
category: computing-software
field: data-engineering
product: prefect
tags: [assets, materialize, asset-deps, asset-keys, lineage]
level: practitioner
status: docs-checked
description: "Track workflow outputs as Prefect assets with the materialize decorator, asset keys, inferred and explicit dependencies, metadata and asset events."
sources:
  - https://docs.prefect.io/v3/concepts/assets
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: record what a workflow produces and what it depends on.

An asset is any outcome or output of a workflow. Its asset key is a URI that uniquely identifies it, often naming an external system. Keys group by scheme (`s3://`, `postgres://`, `snowflake://`) and nest by path. States: materialized, referenced, external.

`@materialize` is a task decorator that records intent to create, update or overwrite an asset; success or failure follows the underlying task.

```python
from prefect.assets import materialize

@materialize("s3://data-lake/processed/customer-data.csv")
def process_customer_data(): ...
```

Dependencies:
- inferred: upstream assets passed through task parameters
- explicit: `asset_deps` for dependencies the task graph does not capture

```python
@materialize("s3://warehouse/enriched-data.csv",
             asset_deps=["postgres://db/reference-tables",
                         "s3://external/vendor-data.csv"])
def enrich_data(): ...
```

The backend tracks dependencies across workflow boundaries.

Metadata: `AssetProperties` holds name, description (Markdown), owners and URL. Materializing with properties fully overwrites all metadata fields, so keep one source of truth. `add_asset_metadata()` attaches runtime metadata such as row counts to materialization events.

Events: `prefect.asset.materialization.succeeded` and `.failed` for downstream assets; `prefect.asset.referenced` for upstream assets, always emitted on materialization. Cached states emit no asset events.

## Checked

2026-11-09. Confirmed: Assets page (docs.prefect.io/v3/concepts/assets): asset key, three states, @materialize, inferred and asset_deps dependencies, AssetProperties, add_asset_metadata(), event names and emission rules. Nothing removed.

Method: documentation only; no commands were run.
