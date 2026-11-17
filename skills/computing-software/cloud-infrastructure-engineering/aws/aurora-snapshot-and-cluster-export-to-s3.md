---
id: computing-software.cloud-infrastructure-engineering.aws.aurora-snapshot-and-cluster-export-to-s3
name: aurora-snapshot-and-cluster-export-to-s3
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, aurora, snapshot-export-s3, export-to-s3, parquet, data-lake]
level: advanced
status: docs-checked
description: "Export Aurora and RDS snapshots or live cluster data to S3 as Parquet for analytics, with the IAM role, KMS key and table filters, plus query-level S3 exports."
sources: ["https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/aurora-export-snapshot.html", "https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/export-cluster-data.html", "https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/postgresql-s3-export.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Exporting snapshots and cluster data to S3

## 1. Snapshot or cluster export (Parquet)
```bash
aws rds start-export-task --export-task-identifier orders-2026-10-18 \
  --source-arn <CLUSTER_SNAPSHOT_ARN> \
  --s3-bucket-name db-exports-<ACCOUNT_ID> --s3-prefix orders/ \
  --iam-role-arn arn:aws:iam::<ACCOUNT_ID>:role/rds-s3-export \
  --kms-key-id arn:aws:kms:<REGION>:<ACCOUNT_ID>:key/<KEY_ID> \
  --export-only orders.public.orders orders.public.order_items
aws rds describe-export-tasks --export-task-identifier orders-2026-10-18 --query 'ExportTasks[].{s:Status,p:PercentProgress}'
```
- `--source-arn` is the ARN of the snapshot (manual or automated system snapshot; find it with
  `aws rds describe-db-cluster-snapshots`) or, for a live cluster export, the DB cluster ARN
  (`arn:aws:rds:<REGION>:<ACCOUNT_ID>:cluster:<NAME>`). Aurora clones the cluster and exports from the clone; the
  cluster export is charged for the whole cluster even for a partial export.
- `--export-only` takes `database`, `database.schema` or `database.schema.table` identifiers (PostgreSQL) as listed on the
  export pages; by default everything is exported. The bucket must be in the same Region as the snapshot or cluster.
- Role: trust `export.rds.amazonaws.com`; `s3:PutObject*`, `s3:GetObject*`, `s3:ListBucket`, `s3:DeleteObject*`,
  `s3:GetBucketLocation` on the bucket and its objects.
- `--kms-key-id` is required by the API (symmetric encryption key); its key policy must include `kms:CreateGrant`
  and `kms:DescribeKey`, and any deny statement must exclude `export.rds.amazonaws.com`.
- The export runs in the background without affecting the active cluster. Exports are Parquet files, usually 1-10 MB each.

## 2. Query it
Output is Apache Parquet in the target bucket; query it with Athena or Redshift Spectrum (the export pages
point to both) after cataloguing it, for example with a Glue crawler. Check the User Guide's data type mapping for
numeric and date columns.

## 3. Query-level exports
- Aurora PostgreSQL: `SELECT * FROM aws_s3.query_export_to_s3('SELECT ...', aws_commons.create_s3_uri('bucket','path','<REGION>'), options :='format csv');`
  (needs the `aws_s3` extension and an IAM role associated with the cluster for the `s3Export` feature; `options` carries
  PostgreSQL `COPY` arguments).
- Aurora MySQL: `SELECT ... INTO OUTFILE S3 's3-<REGION>://bucket/path' FORMAT CSV;` (also `FIELDS TERMINATED BY`); for
  Aurora MySQL version 3 and 8.4 set the `aws_default_s3_role` cluster parameter to the IAM role ARN (version 2 also
  supports `aurora_select_into_s3_role`).

## Verify
- [ ] Athena row count for a table matches `SELECT count(*)` at the snapshot time.

## Checked
Date: 2026-10-27. Sources: Aurora User Guide pages aurora-export-snapshot, export-cluster-data (and .Setup, .Exporting),
postgresql-s3-export and postgresql-s3-export-functions, AuroraMySQL.Integrating.SaveIntoS3; botocore `rds` model
(StartExportTask required members). Corrected the billing claim (charged for the whole cluster, not "per GB of snapshot
scanned"), replaced the unconfirmed snapshot ARN, clarified KMS requirements and added the MySQL role parameters.
Method: documentation only; no commands were run.
