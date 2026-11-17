---
id: computing-software.data-engineering.data-quality.dataplex-and-cloud-governance-catalogs
name: dataplex-and-cloud-governance-catalogs
category: computing-software
field: data-engineering
product: data-quality
tags: [data-quality, dataplex, cloud-data-catalog, data-governance, data-profiling]
level: advanced
status: draft
description: "Use cloud governance catalogs like Google Dataplex Universal Catalog (and peers such as Purview, Glue/DataZone): discovery, aspects, data quality scans, lineage, and governance."
sources:
  - https://cloud.google.com/dataplex/docs/introduction
  - https://cloud.google.com/dataplex/docs/auto-data-quality-overview
  - https://learn.microsoft.com/en-us/purview/purview
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Dataplex and cloud governance catalogs

**Goal:** a managed, cloud-native catalog with discovery, business metadata, quality checks and lineage for data across the platform.

## Dataplex (Google Cloud) building blocks
- **Universal Catalog**: automatic metadata for BigQuery, Cloud Storage, Spanner, Bigtable, Pub/Sub, etc.; search across projects.
- **Aspects and aspect types**: structured custom metadata (owner, tier, sensitivity) with schemas, attached to entries; glossaries for business terms.
- **Data profiling scans**: per-column stats (nulls, distinct, top values, ranges) on BigQuery tables.
- **Auto data quality scans**: declarative rules (non-null, range, regex, set, uniqueness, SQL row/aggregate conditions) with thresholds; results to BigQuery and Cloud Logging for alerting.
- **Lineage**: automatic for BigQuery jobs, Dataflow, Composer (OpenLineage), Dataproc.
- **Lakes/zones** (older Dataplex model) for organising storage with policies.

```bash
gcloud dataplex datascans create data-quality orders-dq \
  --location=europe-west1 \
  --data-source-resource="//bigquery.googleapis.com/projects/acme/datasets/core/tables/orders" \
  --data-quality-spec-file=orders_dq.yaml \
  --schedule="TZ=UTC 0 6 * * *"
```
```yaml
# orders_dq.yaml
rules:
  - column: order_id
    dimension: UNIQUENESS
    uniquenessExpectation: {}
  - column: amount
    dimension: VALIDITY
    rangeExpectation: {minValue: "0"}
    threshold: 0.99
```

## Peers on other clouds
- **Microsoft Purview**: data map scanning, classification, data estate insights, data quality (Unified Catalog).
- **AWS**: Glue Data Catalog (technical), Amazon DataZone / SageMaker Catalog (business catalog, subscriptions), Glue Data Quality (DQDL rules).
- Platform catalogs: Unity Catalog (Databricks), Snowflake Horizon.

## Choosing
Use the cloud's catalog when most data lives in that cloud and you want managed integration; use a cross-platform catalog (DataHub, OpenMetadata, Collibra, Atlan) when you span clouds/tools and need richer workflows.

## Gotchas
- Scans cost query/processing charges: sample large tables, schedule sensibly.
- Business metadata needs owners; automatic discovery fills only technical metadata.

## Verify
Quality scan results land in the configured BigQuery table and a failing rule raises an alert; catalog search finds assets by aspect values.
