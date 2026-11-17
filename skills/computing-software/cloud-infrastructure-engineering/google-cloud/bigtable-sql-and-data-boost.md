---
id: computing-software.cloud-infrastructure-engineering.google-cloud.bigtable-sql-and-data-boost
name: bigtable-sql-and-data-boost
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, bigtable, bigtable-sql, bigtable-data-boost, analytics, app-profiles]
level: practitioner
status: docs-checked
description: "Query Bigtable with GoogleSQL from Bigtable Studio or clients, and offload batch reads to Data Boost serverless compute so analytics never touches serving nodes."
sources: ["https://docs.cloud.google.com/bigtable/docs/googlesql-overview", "https://docs.cloud.google.com/bigtable/docs/data-boost-overview", "https://docs.cloud.google.com/sdk/gcloud/reference/bigtable/app-profiles/create", "https://docs.cloud.google.com/bigtable/docs/metrics"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bigtable SQL and Data Boost

## 1. GoogleSQL on Bigtable
Each column family appears as a map column keyed by column qualifier (bytes keys and values; the latest cell by default); `_key` is the row key.
```sql
SELECT _key, CAST(cf1['status'] AS STRING) AS status
FROM events
WHERE _key BETWEEN 'user#123#' AND 'user#123#~'
LIMIT 100;
```
- Filter on `_key`: SQL runs on the cluster nodes like NoSQL requests, so avoid full table scans and keep queries targeted with `_key` filters.
- `with_history => TRUE` returns all stored versions (each column becomes an array of timestamp/value structs, newest first); `as_of => TIMESTAMP(...)` returns the latest values at or before a time; `CAST` decodes bytes.
- Run in Bigtable Studio (console) or via the client `executeQuery` API (Java, Python, Go); continuous materialized views and logical views build on the same SQL.
- Only `SELECT` is supported: no DDL, `JOIN`, `UNION`, subqueries or CTEs. List column family IDs explicitly in production queries instead of `SELECT *`.

## 2. Data Boost
Serverless read compute isolated from your clusters, billed in serverless processing units (SPUs; 1,000 SPUs equal one node in performance, minimum 60 SPU-seconds and at least 10 SPUs per second per request).
```bash
gcloud bigtable app-profiles create analytics --instance=<I> \
  --route-to=<CLUSTER> --data-boost --data-boost-compute-billing-owner=HOST_PAYS
```
- Use this app profile from Dataflow (Beam `BigtableIO` 2.54.0 or later), Spark, BigQuery external tables, or SQL (Enterprise Plus).
- Built for high-throughput scans, not point reads or reverse scans; read-only (no writes or deletes). Data written or replicated more than 35 minutes before a read is readable; newer data is not guaranteed.
- Requires the Enterprise or Enterprise Plus edition; HDD and tiered storage are available only with Enterprise Plus.
- Not supported with multi-cluster routing, request priorities, single-row transactions, change streams, CMEK instances or regional endpoints; not covered by the Bigtable SLA.

## Gotchas
- SQL queries without a key filter on big tables consume node CPU; consider a Data Boost profile for analytical scans.
- Column qualifiers and values are bytes; mixed encodings need explicit decoding.

## Verify
- [ ] During an analytics job, cluster CPU stays flat and the Data Boost SPU usage metric (see the Bigtable metrics list) rises.

## Checked
Checked 2026-10-24 against the Bigtable GoogleSQL overview, Data Boost overview, metrics page and the gcloud `bigtable app-profiles create` reference (docs.cloud.google.com). Confirmed `_key`, `with_history`, `as_of`, supported statements and limits, `--data-boost` with `--data-boost-compute-billing-owner` (only `HOST_PAYS` is supported), SPU billing, the 35-minute consistency window, edition requirements and the unsupported-feature list. Removed `TO_INT64`, the `bigtable.appProfiles.get` permission claim and the exact Data Boost metric name (the documentation pages read disagree on it). The tiered-storage and SQL edition notes come from the Data Boost page.
Method: documentation only; no commands were run.
