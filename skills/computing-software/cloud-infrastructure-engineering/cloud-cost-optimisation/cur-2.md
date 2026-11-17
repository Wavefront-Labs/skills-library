---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.cur-2
name: cur-2
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, cost-data-ingestion, cur-2, aws-data-exports, cost-and-usage-report, focus-export, athena-cur]
level: practitioner
status: docs-checked
description: "Set up AWS Data Exports (CUR 2.0 and FOCUS exports) to S3 as Parquet with resource IDs and split cost data, query with Athena; migrate from legacy CUR."
sources: ["https://docs.aws.amazon.com/cur/latest/userguide/what-is-data-exports.html", "https://docs.aws.amazon.com/cur/latest/userguide/table-dictionary-cur2.html", "https://docs.aws.amazon.com/cur/latest/userguide/dataexports-create-standard.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AWS Data Exports (CUR 2.0 / FOCUS)

## Export types
Data Exports offers a standard data export with four tables, plus a cost and usage dashboard
(QuickSight) and a legacy CUR export:
- **CUR 2.0**: the recommended way to receive detailed cost and usage data. Fixed set of columns
  (legacy CUR columns varied month to month with usage, cost categories and tags); some columns are
  collapsed into key-value columns, and the nested keys can optionally be queried as separate
  columns to match the legacy schema. The SQL table name is `COST_AND_USAGE_REPORT`.
- **FOCUS 1.2 with AWS columns** and **FOCUS 1.0 with AWS columns**: FOCUS-shaped exports for
  multi-cloud normalisation (no table configuration options).
- **Cost optimization recommendations** (from Cost Optimization Hub; needs a service-linked role)
  and **Carbon emissions** (needs the `sustainability:GetCarbonFootprintSummary` permission).
- Console exports pick columns; CLI/SDK exports can use SQL (select columns, filter rows, rename).

## CUR 2.0 table configurations
`TIME_GRANULARITY` (HOURLY, DAILY, MONTHLY), `INCLUDE_RESOURCES` (adds `line_item_resource_id` and
one line item per resource; can greatly raise row count and file size),
`INCLUDE_SPLIT_COST_ALLOCATION_DATA` (adds `split_line_item_*` columns for ECS tasks and Kubernetes
pods), `INCLUDE_CAPACITY_RESERVATION_DATA`, `INCLUDE_IAM_PRINCIPAL_DATA` and
`INCLUDE_MANUAL_DISCOUNT_COMPATIBILITY` (only for customers on the Discount Automation program).

## Setup
1. Billing and Cost Management console -> Data Exports -> Create export -> Standard data export.
   Export names: up to 128 characters, unique, letters, digits, hyphen and underscore.
2. Choose the CUR 2.0 table; pick billing view, include resource IDs, split cost allocation data
   (containers), and time granularity.
3. Refresh cadence for billing exports is daily (refreshed up to once per day). File versioning:
   overwrite (saves S3 storage) or create new files (lets you track changes over time).
4. Report data integration: Athena selects Parquet with overwrite and delivers a setup script;
   Redshift selects gzip CSV. Formats: Parquet, gzip text/csv, zip text/csv.
5. Pick the S3 bucket (this or another account). Choosing an existing bucket means Data Exports
   overwrites its bucket policy with one that lets both CUR and Data Exports deliver. Use a path
   prefix unique to your account when delivering to another account's bucket.
6. Optional: up to 50 tags on the export.

## Organizations behaviour
A management account's export covers all member accounts; a member account's export covers only
that account, and only for the time it has been a member. A departed member can still read previous
exports it has S3 permissions for. Create exports in the management account for the full picture.

## Migration from legacy CUR
CUR 2.0 has a different, fixed schema with nested key-value columns and extra columns such as
`bill_payer_account_name` and `line_item_usage_account_name`. Update queries and dashboards, and run
both in parallel for a period to reconcile totals. AWS documents the path as "Migrating from CUR to
Data Exports CUR 2.0".

## Gotchas
- Resource IDs and split cost allocation data both multiply line items; watch export size.
- Legacy CUR uses a different set of IAM actions than Data Exports.

## Verify
- [ ] Monthly total from the export matches the invoice (allowing for tax/credits handling).

## Checked

Method: docs-checked 2026-11-09 against the AWS Data Exports pages what-is-data-exports, dataexports-create-standard and table-dictionary-cur2. Removed unconfirmed: "delivered several times a day", month restatement behaviour, bucket policy principal name, Glue crawler step, example SQL and product column names, tag activation note.
