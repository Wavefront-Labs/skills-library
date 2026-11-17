---
id: computing-software.data-engineering.etl-pipeline-design.bulk-data-transfer-options
name: bulk-data-transfer-options
category: computing-software
field: data-engineering
product: etl-pipeline-design
tags: [etl-pipeline-design, data-migration, bulk-transfer, storage-transfer-service, aws-datasync, snowball, azcopy, rclone, parallel-export, egress-cost]
level: practitioner
status: draft
description: "Move terabytes to petabytes between systems: export formats, online transfer services, offline appliances, parallel unload, network maths, egress costs and integrity checks."
sources:
  - https://cloud.google.com/storage-transfer/docs/overview
  - https://docs.aws.amazon.com/datasync/latest/userguide/what-is-datasync.html
  - https://aws.amazon.com/snowball/
  - https://learn.microsoft.com/en-us/azure/storage/common/storage-use-azcopy-v10
  - https://rclone.org/docs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Bulk data transfer options

**Goal:** move historical data for a migration within the time window and budget, with proof nothing was lost.

## 1. Do the network maths first
Transfer time ≈ bytes / (bandwidth × utilisation). At 1 Gbps with ~80% use: ~8.6 TB/day. 100 TB ≈ 12 days. At 10 Gbps: ~86 TB/day.
Rule of thumb: if the online transfer takes more than ~1-2 weeks, consider an offline appliance or a bigger link (Direct Connect / Interconnect / ExpressRoute).

## 2. Path per source
| From → to | Tool |
|---|---|
| Object store → object store, cross-cloud | GCP Storage Transfer Service, AWS DataSync, AzCopy (`azcopy copy` from S3/GCS), rclone |
| On-prem NFS/HDFS → cloud | DataSync agent, Storage Transfer agents, `hadoop distcp` to s3a://, gs:// |
| Offline (no bandwidth) | AWS Snowball Edge, Azure Data Box, Google Transfer Appliance |
| Database → warehouse | unload to files (parallel) then bulk load; avoid row-by-row JDBC |
| Warehouse → warehouse | `UNLOAD`/`COPY INTO @stage`/`EXPORT DATA` to Parquet in object storage, then `COPY`/`LOAD` |

## 3. Unload in parallel, in a columnar format
```sql
-- Redshift
UNLOAD ('SELECT * FROM sales WHERE sale_date >= ''2024-01-01''')
TO 's3://mig-bucket/sales/' IAM_ROLE '<role-arn>' FORMAT PARQUET PARTITION BY (sale_date) MAXFILESIZE 256 MB;
-- Snowflake
COPY INTO @mig_stage/sales/ FROM sales PARTITION BY (TO_VARCHAR(sale_date)) FILE_FORMAT=(TYPE=PARQUET) MAX_FILE_SIZE=268435456;
-- BigQuery
EXPORT DATA OPTIONS(uri='gs://mig-bucket/sales/*.parquet', format='PARQUET') AS SELECT * FROM ds.sales;
```
- Parquet keeps types and compresses 3-10x vs CSV; CSV loses types (timestamps, decimals, NULL vs '').
- Target 100 MB-1 GB files: thousands of tiny files slow both transfer and load.
- Partition the export by date so you can resume and reconcile per partition.

## 4. Cost
- Egress from a cloud is typically charged per GB leaving the region/provider; 500 TB of internet egress is a significant line item. Check provider migration programmes/egress waivers before starting.
- Same-region transfers between services are usually free or cheap; cross-region is not.
- Transfer service fees (per GB for DataSync; appliance rental per job) add up — include in the plan.

## 5. Integrity
- Use tools that verify checksums (DataSync and Storage Transfer verify by default; `rclone check` / `rclone copy --checksum`; AzCopy `--check-md5`).
- Keep a manifest (path, size, row count) from the source; compare after load, then run table reconciliation.
- Make the copy resumable (sync semantics) — big transfers always get interrupted.

## Verify
- [ ] Timeline uses measured, not nominal, bandwidth from a test transfer.
- [ ] Egress cost estimate is approved.
- [ ] Manifest file/row counts match after load; reconciliation passes per partition.
