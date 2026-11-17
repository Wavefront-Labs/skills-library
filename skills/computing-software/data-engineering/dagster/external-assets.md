---
id: computing-software.data-engineering.dagster.external-assets
name: external-assets
category: computing-software
field: data-engineering
product: dagster
tags: [dagster, external-assets, assetspec, report-asset-materialization, rest-api, sensor]
level: practitioner
status: docs-checked
description: "Model assets orchestrated elsewhere as Dagster external assets and report their materializations via sensors or the REST API."
sources:
  - https://docs.dagster.io/guides/build/assets/external-assets
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# External assets

Goal: show assets produced by other systems (files in a data lake populated by an internal tool, a CSV delivered daily by SFTP, a table populated by another orchestrator) in Dagster lineage, and build downstream assets on them.

Unlike native assets, Dagster cannot materialize external assets directly or put them in a schedule. An external system must inform Dagster when one is updated.

## Define
Use `AssetSpec` (docs example: a `raw_transactions` asset from partner SFTP data). Like regular assets, external assets can have dependencies, so a whole pipeline orchestrated by another system can be modeled as a graph.

## Record materializations and metadata
Tell Dagster whenever the external asset is updated, with relevant metadata such as last-updated time. Two ways:
1. Pull with a sensor that regularly polls the external system (the docs poll an SFTP server and update the asset when the file changes).
2. Push to the REST API from the external system.

Dagster+ (authentication header required; request goes to your org and a deployment):

```shell
curl -X POST \
  -H 'Content-Type: application/json' \
  -H 'Dagster-Cloud-Api-Token: [YOUR API TOKEN]' \
  'https://[YOUR ORG NAME].dagster.cloud/[YOUR DEPLOYMENT NAME]/report_asset_materialization/' \
  -d '{"asset_key": "raw_transactions", "metadata": {"file_last_modified_at_ms": 1724614700266}}'
```

OSS needs no authentication headers; point at your open source URL, `http://localhost:3000/report_asset_materialization/` in the docs example.

## Checked
2026-11-08. Confirmed against the Dagster docs page External assets (raw markdown from the docs repo): definition, use cases, sensor and REST push methods, both curl examples (condensed to one line), graph modeling. Snippets referenced by file were not read. Nothing removed.
Method: documentation only; no commands were run.
