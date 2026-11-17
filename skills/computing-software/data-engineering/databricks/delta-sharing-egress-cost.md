---
id: computing-software.data-engineering.databricks.delta-sharing-egress-cost
name: delta-sharing-egress-cost
category: computing-software
field: data-engineering
product: databricks
tags: [databricks, delta-sharing, sharing-egress-cost, cross-region-sharing, cloudflare-r2, data-replication, finops, cloud-egress]
level: practitioner
status: docs-checked
description: "Control Delta Sharing (OpenSharing) egress costs as a provider: who pays, replicating to the recipient's region, Cloudflare R2, monitoring."
sources:
  - https://docs.databricks.com/aws/en/opensharing/manage-egress
  - https://docs.databricks.com/aws/en/opensharing
  - https://developers.cloudflare.com/r2/pricing/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Delta Sharing egress cost

**Goal:** share data with recipients in other regions or clouds without an unbounded data-transfer bill landing on the provider.

## 1. Who pays
Current Databricks docs call the feature OpenSharing (Delta Sharing). It does not replicate data: recipients read the shared files from the provider's storage through pre-signed short-lived URLs.
- Sharing within a region incurs no egress cost.
- Sharing across clouds or regions can incur data egress fees from the cloud vendor, which the provider bears.
- If the provider uses SecureConnect, Databricks bills the data transfer instead of the cloud vendor.
Each recipient scan reads those bytes again, so a dashboard that refreshes often on a large shared table multiplies the transfer.

## 2. Reduce bytes read
- Share **aggregated or filtered** tables (gold), not raw history.
- Enable change data feed on the table and share it `WITH HISTORY`, so recipients merge changes into a local copy instead of re-scanning; egress is then limited to refreshing that copy.
- Recipients should use VPC gateway or interface endpoints for S3 rather than NAT gateways for in-region storage access.

## 3. Move data closer to the recipient
- **Replicate into the recipient's region**: use `DEEP CLONE` to replicate Delta tables to external locations in the regions you share to, and share the replica. Deep clone identifies new data in the source and refreshes the target, so egress is limited to the refresh.
```sql
CREATE OR REPLACE TABLE eu_west_catalog.share.orders DEEP CLONE prod.sales.orders;   -- rerun to sync incrementally
```
Schedule the clone as a Databricks job to refresh the replica incrementally.
- **Zero-egress storage**: Cloudflare R2 has no egress fees (also stated on the R2 pricing page). Create an R2 bucket, a storage credential and an external location, create a catalog with the `r2://` managed location, `DEEP CLONE` the tables into it and share those. Limits: R2 tables that use liquid clustering and V2 checkpoint cannot be shared, and view sharing may still incur egress. R2 storage and operations are billed by Cloudflare: see its pricing page.

## 4. Monitor
- Cloud billing: filter data-transfer line items by the storage bucket/account used for shared tables (tag buckets).
- Databricks Marketplace listing OpenSharing Egress Pipeline: two notebooks (IP Ranges Mapping, Egress Cost Analysis) that run as Lakeflow pipelines and report egress bytes by share and recipient.
- Set budget alerts on the data-transfer cost category.

## 5. Contract it
For large external recipients, agree in the data-sharing agreement who covers transfer costs, refresh frequency, and expected query volume.

## Verify
- [ ] Every shared table's bucket is tagged so its transfer cost is visible.
- [ ] Cross-cloud recipients read from a replica in their region or from zero-egress storage.
- [ ] Per-recipient query volume is reviewed monthly.

## Checked

2026-11-09. Confirmed on the Databricks OpenSharing egress page, the OpenSharing overview FAQ and the Cloudflare R2 pricing page: no egress within a region, cross-cloud or cross-region egress fees from the cloud vendor, SecureConnect billed by Databricks, pre-signed short-lived URLs, DEEP CLONE incremental refresh, CDF plus WITH HISTORY, R2 no egress fees, R2 limits (liquid clustering, V2 checkpoint, view sharing), the Marketplace egress pipeline notebooks. Removed: per-GB cost tiers, the 100 GB example, partitioning and Z-order advice, audit action names and the Databricks-to-Databricks compute claim (not on the pages read).

Method: documentation only; no commands were run.

