---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.azure-cost-export
name: azure-cost-export
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, data-ingestion, azure-cost-export, azure-cost-management, cost-exports, focus-export, azure, parquet]
level: practitioner
status: docs-checked
description: "Set up Azure Cost Management exports for a FinOps pipeline: scope choice, FOCUS vs actual/amortised datasets, Parquet, partitions and manifests, backfill and overwrite behaviour."
sources: ["https://learn.microsoft.com/azure/cost-management-billing/costs/tutorial-improved-exports", "https://learn.microsoft.com/azure/cost-management-billing/dataset-schema/schema-index", "https://learn.microsoft.com/cloud-computing/finops/toolkit/hubs/finops-hubs-overview"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Azure Cost Management exports

Exports write cost datasets on a schedule to a storage account; they are the supported bulk path
into a warehouse (the Cost Details API and portal downloads do not scale).

## Choose the scope
Exports can be created at subscription, resource group, management group, department and enrollment
scopes, and at MCA billing account, billing profile and invoice section scopes. The reservation
datasets and price sheet are supported only at the EA billing account or, for other agreements, the billing
profile. Management group exports support usage charges only (no purchases, no amortised cost, no FOCUS,
and no multiple currencies) and are for EA only. Pick the scope that matches the dataset you need.

## Choose the datasets
| Dataset | Use |
|---|---|
| Cost and usage details (FOCUS) | default for multi-cloud; combines actual and amortised; EA and MCA only, not MOSA |
| Cost and usage details (actual) | standard usage and purchase charges |
| Cost and usage details (amortized) | showback with reservation/savings plan spread |
| Price sheet | the organisation's Azure pricing |
| Reservation details / recommendations / transactions | commitment management |

## Steps
1. Create a storage account (blob or file storage; not a container that is the target of an object
   replication rule). If it has a firewall, enable "Allow trusted Azure services access"; Cost Management
   creates a system-assigned managed identity for the export and needs role-assignment permission on the
   storage account when you create or edit the export.
2. Cost Management -> Exports -> Create: choose a template, then dataset, dataset version and frequency.
   For cost and usage details choose **daily export of month-to-date costs** plus a **monthly export of
   last month's costs** for finalised data. Each export runs on UTC, data is normally available within
   4 hours of a run starting, and for the first five days of a month a daily cost export also runs a hidden
   second job that refreshes the prior month's file, because latent charges can land up to 72 hours after month end.
3. Format **Parquet** with Snappy compression (or CSV with Gzip). Parquet is not offered for the
   reservation datasets. File partitioning is on by default and cannot be disabled; **overwrite data** is on by
   default and replaces the previous day's file in a daily export.
4. Layout: every run writes data partitions (each uncompressed file under 1 GB) plus a `manifest.json`
   listing the blobs, row counts and run id. Always read the manifest for the file names and
   sequence rather than guessing partition names.
5. Backfill: "Export selected dates" reruns an export for past months, one month per run, up to 13 months in
   the portal (not available for price sheets; reservation recommendations are a current snapshot only). The
   Exports - Execute REST API goes further back (up to 7 years for cost and usage and reservation transactions).
6. Ingest: use a tool that handles multi-file ingestion (Power BI, Spark, Fabric); replace the month in
   the warehouse. The Microsoft FinOps toolkit's FinOps hubs build on exports and add Data Factory
   ingestion, Parquet conversion, and Data Explorer or Fabric storage.

```bash
az costmanagement export list --scope "/providers/Microsoft.Billing/billingAccounts/<id>"
```

## Gotchas
- Ingest every partition listed in the manifest; one file is only part of the dataset.
- Dataset schemas are published per agreement type (EA, MCA, MPA, CSP, MOSA) while FOCUS covers EA and MCA, so
  FOCUS gives one schema across those two.
- You choose the dataset schema version when creating an export; version your ingestion mapping.
- In the new export experience, missing attributes such as subscription IDs are null or empty rather than
  the all-zero GUID.
- Do not rely on the exact run time; allow up to 24 hours after creating an export for data.

## Verify
- [ ] Monthly export total equals the invoice for the billing profile.
- [ ] Re-ingesting a month leaves totals unchanged.

## Checked
Date: 2026-11-08. Confirmed against the Azure "Create and manage Cost Management exports" tutorial (read in full),
the dataset schema index and the FinOps hubs overview; the CLI command exists in the Azure CLI reference model used by
the review tooling. Removed the unsupported ADLS Gen2 requirement, the invented date-range folder path, the CSP price
claim and the claim that subscription scope misses purchases. Corrected partitioning (not optional) and backfill limits.
Method: documentation only; no commands were run.
