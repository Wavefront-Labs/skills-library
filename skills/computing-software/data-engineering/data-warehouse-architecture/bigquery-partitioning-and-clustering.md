---
id: computing-software.data-engineering.data-warehouse-architecture.bigquery-partitioning-and-clustering
name: bigquery-partitioning-and-clustering
category: computing-software
field: data-engineering
product: data-warehouse-architecture
tags: [data-warehouse-architecture, partitioning, clustering, bigquery, bigquery-partitioning, bigquery-clustering, require-partition-filter, partition-expiration, cost-control]
level: practitioner
status: gated
description: "Partition and cluster BigQuery tables: time-unit, ingestion-time and integer-range partitions, require_partition_filter, expiration, cluster column order, limits, bytes scanned."
sources:
  - https://cloud.google.com/bigquery/docs/partitioned-tables
  - https://cloud.google.com/bigquery/docs/clustered-tables
  - https://cloud.google.com/bigquery/docs/querying-partitioned-tables
  - https://cloud.google.com/bigquery/quotas#partitioned_tables
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# BigQuery partitioning and clustering

**Goal:** queries scan (and on-demand pricing bills) only the data they need, and old data ages out automatically.

## 1. Partitioning options
```sql
-- time-unit column partitioning (most common)
CREATE TABLE sales.orders (order_id INT64, customer_id INT64, amount NUMERIC, created_at TIMESTAMP, region STRING)
PARTITION BY DATE(created_at)                      -- or TIMESTAMP_TRUNC(created_at, HOUR | MONTH | YEAR)
CLUSTER BY customer_id, region
OPTIONS (require_partition_filter = TRUE, partition_expiration_days = 730);

-- ingestion-time partitioning: pseudo-columns _PARTITIONTIME / _PARTITIONDATE
CREATE TABLE raw.events (payload JSON) PARTITION BY _PARTITIONDATE;

-- integer-range partitioning
CREATE TABLE crm.accounts (account_id INT64, ...)
PARTITION BY RANGE_BUCKET(account_id, GENERATE_ARRAY(0, 10000000, 10000));
```
- Partition limit per table: 10,000 partitions per the quotas page (daily = about 27 years; hourly fills fast — use hourly only with expiration). Above the limit, use clustering in addition to or instead of partitioning.
- Partitioning can't be changed in place; recreate with `CREATE TABLE ... PARTITION BY ... AS SELECT` and swap.
- If partitioning would leave a small amount of data per partition (the docs say approximately less than 10 GB), use clustering instead of, or with coarser, partitioning: many small partitions increase table metadata and can slow metadata access.

## 2. Pruning rules
- Filter the partitioning column with constant expressions: `WHERE created_at >= TIMESTAMP('2026-10-01')` or `DATE(created_at) = '2026-10-16'` prune. Filters through subqueries or on other columns derived from it may not.
- `require_partition_filter = TRUE` rejects queries without a usable partition filter — the best guard against accidental full scans.
- Dry run before running (the `bq query --dry_run` flag (gated: unconfirmed, source is paywalled or blocked)): it estimates bytes processed; for clustered tables you do not get an accurate cost estimate before execution because the blocks scanned are only known at run time.

## 3. Clustering
- Up to **4 columns**; order matters — filter/aggregate columns used most come first (like a sort key prefix).
- Works on high-cardinality columns where partitioning can't (customer_id, sku).
- BigQuery reclusters automatically in the background (the docs describe it as free).
- Changing the clustering spec of an existing table: `bq update --clustering_fields=...` (gated: unconfirmed, source is paywalled or blocked); check the clustered-tables page for how old data is reclustered.
- Filtering on the second cluster column alone helps less than filtering on the first.

## 4. Lifecycle and cost
- `partition_expiration_days` deletes old partitions automatically; dataset-level default expiration exists too.
- Each partition is considered separately for long-term storage pricing, so partitions you stop modifying age into the cheaper rate (the 90-day threshold (gated: unconfirmed, source is paywalled or blocked)); modifying old partitions resets that, so avoid unnecessary rewrites of history.
- Write a single partition atomically with a decorator: `bq query --destination_table 'sales.orders$20261016' --replace ...` or `MERGE` restricted by partition.

## 5. Inspect
The INFORMATION_SCHEMA views and columns below (gated: unconfirmed, source is paywalled or blocked).
```sql
SELECT partition_id, total_rows, total_logical_bytes, last_modified_time
FROM sales.INFORMATION_SCHEMA.PARTITIONS WHERE table_name = 'orders' ORDER BY partition_id DESC;
-- bytes billed by query over time
SELECT user_email, query, total_bytes_billed FROM `region-eu`.INFORMATION_SCHEMA.JOBS
WHERE creation_time > TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 1 DAY) ORDER BY total_bytes_billed DESC LIMIT 20;
```

## Verify
- [ ] Large fact tables have `require_partition_filter = TRUE`.
- [ ] Typical dashboard query's bytes processed drops after partitioning/clustering (compare dry runs).
- [ ] Partition count is well below the limit, with expiration where history isn't needed.

## Checked

- Date: 2026-11-02.
- Confirmed against: BigQuery partitioned-tables, clustered-tables and querying-partitioned-tables pages and the quotas page (10,000 partitions per table, use clustering when partitions would be small, approximately less than 10 GB per partition, up to four clustering columns, automatic reclustering at no charge, per-partition long-term pricing, no accurate cost estimate for clustered tables, require partition filter option, partitioning types).
- Gated: the 90-day long-term threshold, the bq flag syntax and the INFORMATION_SCHEMA queries (not stated in the fetched pages).
- Not checked and left unstated here: any dollar figures (none are given in the skill).

Method: documentation only; no commands were run.
