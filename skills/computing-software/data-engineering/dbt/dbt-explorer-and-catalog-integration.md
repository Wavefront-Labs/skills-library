---
id: computing-software.data-engineering.dbt.dbt-explorer-and-catalog-integration
name: dbt-explorer-and-catalog-integration
category: computing-software
field: data-engineering
product: dbt
tags: [dbt, dbt-cloud, dbt-explorer, data-catalog, datahub, openmetadata, column-level-lineage, catalog-ingestion, discovery-api, manifest-json]
level: practitioner
status: docs-checked
description: "Make dbt metadata discoverable: dbt Catalog (formerly Explorer) lineage and health views, and ingesting manifest/catalog/run_results artifacts into DataHub or OpenMetadata."
sources:
  - https://docs.getdbt.com/docs/explore/explore-projects
  - https://github.com/datahub-project/datahub/blob/master/metadata-ingestion/docs/sources/dbt/dbt_pre.md
  - https://github.com/datahub-project/datahub/blob/master/metadata-ingestion/docs/sources/dbt/dbt_recipe.yml
  - https://github.com/open-metadata/OpenMetadata/blob/main/openmetadata-ui/src/main/resources/ui/public/locales/en-US/Database/workflows/dbt.md
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# dbt Catalog (formerly Explorer) and catalog integration

**Goal:** people outside the dbt repo can find models, owners, definitions, lineage and test status.

## dbt Catalog (dbt platform)
- Needs a dbt platform Starter, Enterprise or Enterprise+ account, a production or staging deployment environment for each project, and at least one successful job run there. CI jobs do not update Catalog.
- Shows resources (models, seeds, snapshots, sources, exposures and more), lineage, data health signals, and marts and public models.
- Model performance, project recommendations and column-level lineage are Enterprise and Enterprise+ features.
- Core users can upload dbt Core artifacts into the dbt platform to view them in Catalog.

## DataHub (dbt Core artifacts)
```yaml
# recipe.yml
source:
  type: dbt
  config:
    manifest_path: s3://<BUCKET>/dbt/prod-artifacts/manifest.json
    catalog_path: s3://<BUCKET>/dbt/prod-artifacts/catalog.json
    run_results_paths:
      - s3://<BUCKET>/dbt/prod-artifacts/run_results.json   # optional, records dbt test results
    target_platform: snowflake       # platform id of the warehouse the models live in
    meta_mapping:
      business_owner:
        match: ".*"
        operation: add_owner
        config: {owner_type: user}
      data_tier:
        match: ".*"
        operation: add_tag
        config: {tag: "tier"}
sink:
  type: datahub-rest
  config: {server: "https://<DATAHUB_GMS>"}
```
Run `datahub ingest -c recipe.yml`. `manifest_path`, `catalog_path`, `run_results_paths` accept local, S3 or GCS locations (S3 and GCS need connection settings such as `aws_connection`); `sources_path` is optional for freshness. `meta_mapping` is keyed by the dbt `meta` key and each rule has `match`, `operation` (`add_owner`, `add_tag`, `add_term`) and `config`.

## OpenMetadata
The dbt workflow reads `manifest.json` (mandatory), `catalog.json` and `run_results.json` (optional) from one of five sources: local files, an HTTP or file server, the dbt Cloud API (account ID, token, project ID), S3 or GCS.

## Practice
- Ingest artifacts from the production run only, so dev manifests do not pollute the catalog.
- Expose test results (`run_results.json`) so consumers see quality signals next to the table.

## Verify
- [ ] A mart in the catalog shows owner, description, upstream lineage to sources, and last test results.
- [ ] Changes to descriptions appear in the catalog after the next production run and ingestion.

## Checked

2026-10-25: dbt docs (docs.getdbt.com repository, last commit 2026-10-23). Confirmed: dbt Catalog page (plan requirements, prerequisites, Enterprise-only features); DataHub dbt source recipe and configuration (`manifest_path`, `catalog_path`, `sources_path`, `run_results_paths`, `target_platform`, S3/GCS connections, `meta_mapping` operations) and `datahub-rest` sink from the DataHub repository (last commit 2026-10-23); OpenMetadata dbt workflow config sources from the OpenMetadata repository UI docs (last commit 2026-10-24). Removed unconfirmed claims about the Discovery API, mandatory docs generation, warehouse-ingestion ordering and what the OpenMetadata workflow updates.

Method: documentation only; no commands were run.
