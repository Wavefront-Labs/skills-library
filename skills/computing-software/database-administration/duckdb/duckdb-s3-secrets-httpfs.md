---
id: computing-software.database-administration.duckdb.duckdb-s3-secrets-httpfs
name: duckdb-s3-secrets-httpfs
category: computing-software
field: database-administration
product: duckdb
tags: [duckdb, httpfs, s3, secrets, credential-chain, r2, gcs]
level: practitioner
status: docs-checked
description: "Read, glob and write S3-compatible storage from DuckDB with httpfs: config and credential_chain secrets, R2/GCS types, parameters, partitioned writes."
sources:
  - https://raw.githubusercontent.com/duckdb/duckdb-web/main/docs/1.4/core_extensions/httpfs/s3api.md
  - https://raw.githubusercontent.com/duckdb/duckdb-web/main/docs/1.4/data/multiple_files/overview.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: authenticate to S3-API object storage with a secret, then query and write `s3://` paths.

Required S3 API pieces per feature: public reads need HTTP Range; private reads need key or session-token auth; globbing needs ListObjectsV2; writes need multipart upload. Tested on AWS S3, Minio, Google Cloud, lakeFS; R2 and Tigris should work.

Secrets (the preferred method; the legacy S3 settings are deprecated):

```sql
CREATE OR REPLACE SECRET s (TYPE s3, PROVIDER config,
  KEY_ID 'AKIA...', SECRET '...', REGION 'us-east-1');
CREATE OR REPLACE SECRET s (TYPE s3, PROVIDER credential_chain);              -- AWS SDK default chain
CREATE OR REPLACE SECRET s (TYPE s3, PROVIDER credential_chain, CHAIN 'env;config');
CREATE OR REPLACE SECRET s (TYPE s3, PROVIDER credential_chain, CHAIN config, PROFILE 'my_profile');
```
`CHAIN` is a semicolon-separated ordered list from `config`, `sts`, `sso`, `env`, `instance`, `process`. Other parameters override fetched values (for example `REGION`). If you hit `Connection error for HTTP HEAD`, set `ENDPOINT 's3.<region>.amazonaws.com'`.

Parameters (default): `ENDPOINT` (`s3.amazonaws.com`), `KEY_ID`, `SECRET`, `SESSION_TOKEN`, `REGION` (`us-east-1`, must match the bucket), `URL_STYLE` (`vhost` for S3, `path` for R2 and GCS), `USE_SSL` (true), `URL_COMPATIBILITY_MODE` (true), and S3-only `KMS_KEY_ID` (server-side encryption), `REQUESTER_PAYS` (false). R2 adds `ACCOUNT_ID`.

Other types: `TYPE r2` (with `ACCOUNT_ID`, used with `r2://` URLs) and `TYPE gcs` (used with `gcs://` or `gs://`). GCS needs HMAC keys made for interoperability, not service-account keys. With `credential_chain` for R2 or GCS, the AWS client reads `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`, so export your R2 or HMAC keys under those names. The page's KMS example also passes a `SCOPE 's3://<bucket-sub-path>'` clause (see duckdb-secrets-manager).

Read and glob:

```sql
SELECT * FROM 's3://bucket/file.parquet';
SELECT * FROM read_parquet('s3://bucket/folder*/100?/t[0-9].parquet');   -- glob via ListObjectsV2
```
The multi-file docs say the `?` wildcard is not supported for reads over S3 due to HTTP encoding issues (the S3 page itself shows `?` in an example, so test it); `filename = true` adds a `filename` column with the source file. Parquet partial reads (range requests) and Hive partitioning work.

Write (CSV or Parquet; multipart upload):

```sql
COPY tbl TO 's3://bucket/partitioned' (FORMAT parquet, PARTITION_BY (a, b), OVERWRITE_OR_IGNORE true);
```
The existing-file check is conservative and adds latency; `OVERWRITE_OR_IGNORE` skips it. Output names: `s3://bucket/partitioned/part_col_a=<val>/part_col_b=<val>/data_<thread_number>.parquet`. Upload settings (defaults suffice for most uses): `s3_uploader_max_parts_per_file` and `s3_uploader_max_filesize` (used for part size calculation), `s3_uploader_thread_limit` (maximum number of uploader threads).

## Checked

2026-11-07. Read the DuckDB 1.4 docs pages core_extensions/httpfs/s3api.md and data/multiple_files/overview.md in full. Confirmed: tested platforms, feature to S3-API requirement table, config and credential_chain secrets, CHAIN values and the `env;config` example, PROFILE, the HEAD-error ENDPOINT tip, the parameter table and defaults (ENDPOINT, REGION, URL_STYLE, USE_SSL, URL_COMPATIBILITY_MODE, KMS_KEY_ID, REQUESTER_PAYS, ACCOUNT_ID), R2 and GCS secret types, HMAC key requirement, AWS environment variable note, globbing via ListObjectsV2, `filename`, Hive partitioning, multipart writes, OVERWRITE_OR_IGNORE, uploader settings. Changed: removed the unsupported claim that SCOPE limits a secret to a prefix, reworded the `?` glob caveat to cite the multi-file page, completed the output-name pattern, removed the invented Verify step. Added the multi-file overview page to sources.

Method: documentation only; no commands were run.
