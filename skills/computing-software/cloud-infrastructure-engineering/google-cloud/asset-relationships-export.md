---
id: computing-software.cloud-infrastructure-engineering.google-cloud.asset-relationships-export
name: asset-relationships-export
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, cloud-asset-inventory, asset-relationships, relationship-types, dependency-graph, asset-export]
level: practitioner
status: docs-checked
description: "Export Cloud Asset Inventory RELATIONSHIP content to BigQuery, know the relationship table schema and its limits, and query dependency edges for impact analysis."
sources: ["https://docs.cloud.google.com/asset-inventory/docs/exporting-to-bigquery"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Asset relationships export

Cloud Asset Inventory can export **RELATIONSHIP** content: typed edges between assets. Selecting relationship types requires access to the Security Command Center Premium or Enterprise tier. Take valid relationship type names from the Cloud Asset Inventory supported relationship types list in the docs.

## Export
```bash
gcloud asset export --organization=<ORG> --content-type=relationship \
  --relationship-types=<TYPE_1>,<TYPE_2> \
  --bigquery-table=projects/<P>/datasets/cai/tables/rel --output-bigquery-force
```
`--output-bigquery-force` overwrites the destination table; appending needs a partitioned table. The RELATIONSHIP content type cannot be exported with `--per-asset-type`, so you get one table.

## Queries
```sql
-- edges of one relationship type pointing at a given asset
SELECT name, asset_type, related_asset.asset, related_asset.asset_type
FROM `<P>.cai.rel`
WHERE related_asset.relationship_type = '<TYPE_1>'
  AND related_asset.asset LIKE '%/<TARGET_NAME>';
```
The relationship table has columns `name`, `asset_type`, a `related_asset` record (`asset`, `asset_type`, `ancestors`, `relationship_type`), `ancestors` and `update_time`.

## Live lookup
```bash
gcloud asset list --organization=<ORG> --content-type=relationship \
  --relationship-types=<TYPE_1> --asset-types=<ASSET_TYPE> --limit=20
```

## Uses
- Blast radius before deleting a subnet, disk or service account.
- Orphan detection: assets with no edge of the expected relationship type.
- Feeding a CMDB or graph DB.

## Gotchas
- If relationship export fails, check Security Command Center tier access and the supported types list.
- An export is a snapshot; use a partitioned table to append later exports.

## Verify
- [ ] Export table contains edges for a known asset.

## Checked
2026-10-31. Confirmed on "Export asset metadata to BigQuery": `--content-type=relationship`, `--relationship-types` needs SCC Premium or Enterprise, relationship table schema (`related_asset` record with `relationship_type`), `--output-bigquery-force`, RELATIONSHIP cannot use `--per-asset-type`, appending needs partitioned tables. Removed: concrete relationship type names (the supported-types and relationships pages 404), the old query and column names (wrong against the schema), `--partition-key` on a relationship export, scheduling advice. Commands checked with check_commands.py.
Method: documentation only; no commands were run.
