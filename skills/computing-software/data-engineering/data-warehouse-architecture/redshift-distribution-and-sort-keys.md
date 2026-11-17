---
id: computing-software.data-engineering.data-warehouse-architecture.redshift-distribution-and-sort-keys
name: redshift-distribution-and-sort-keys
category: computing-software
field: data-engineering
product: data-warehouse-architecture
tags: [data-warehouse-architecture, partitioning, clustering, amazon-redshift, redshift-distkey, sort-keys, diststyle, zone-maps, data-skew, automatic-table-optimization]
level: practitioner
status: gated
description: "Choose Amazon Redshift distribution styles and sort keys: KEY vs ALL vs EVEN vs AUTO, co-located joins, compound sort keys for zone maps, detecting skew, and altering tables."
sources:
  - https://docs.aws.amazon.com/redshift/latest/dg/c_choosing_dist_sort.html
  - https://docs.aws.amazon.com/redshift/latest/dg/t_Distributing_data.html
  - https://docs.aws.amazon.com/redshift/latest/dg/t_Sorting_data.html
  - https://docs.aws.amazon.com/redshift/latest/dg/t_Creating_tables.html
  - https://docs.aws.amazon.com/redshift/latest/dg/r_SVV_TABLE_INFO.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Redshift distribution and sort keys

**Goal:** joins run without redistributing data across nodes, range filters skip blocks, and no slice does all the work.

## 1. Distribution styles
| Style | Rows placed | Use for |
|---|---|---|
| `KEY` (`DISTKEY(col)`) | by hash of the column | large fact + its most-joined large dimension on the same key → co-located join |
| `ALL` | full copy on every node | small, slowly changing dimensions (copy cost × nodes on every write) |
| `EVEN` | round-robin | tables not joined, or no good key |
| `AUTO` (default) | Redshift assigns a style from table size (initially ALL for small tables) and can change it over time | when unsure; let automatic table optimization decide |

Good DISTKEY: the join column of the biggest join, high cardinality, evenly distributed, not commonly filtered to a single value (filtering one value = one slice works).
Bad DISTKEY: low cardinality (country), skewed (a NULL/default value with millions of rows), date columns (today's data on one slice).

## 2. Sort keys
- Redshift keeps min/max **zone maps** per 1 MB block (gated: unconfirmed, source is paywalled or blocked); a sort key makes range filters skip blocks.
- **Compound** sort key (default): order columns by how queries filter — usually the date/timestamp first. Prefix matters: filters on the 2nd column alone get little benefit.
- Interleaved sort keys: equal weight to each column, but expensive maintenance (`VACUUM REINDEX`) and poor for monotonically increasing columns (gated: unconfirmed, source is paywalled or blocked) — rarely worth it.
- `SORTKEY AUTO` lets Redshift choose.
- Sort and dist key on the same join column enables merge joins for large-large joins.

```sql
CREATE TABLE sales.fact_orders (
  order_id BIGINT, customer_id BIGINT, order_date DATE, amount DECIMAL(18,2))
DISTSTYLE KEY DISTKEY (customer_id)
COMPOUND SORTKEY (order_date, customer_id);

CREATE TABLE sales.dim_region (...) DISTSTYLE ALL;
```

## 3. Read the evidence
```sql
SELECT "table", diststyle, sortkey1, skew_rows, unsorted, stats_off, tbl_rows
FROM svv_table_info ORDER BY size DESC LIMIT 30;
```
- `skew_rows` (ratio of rows in the fullest slice to the emptiest) well above 1 → bad distkey; the cut-off of about 4 is a rule of thumb (gated: unconfirmed, source is paywalled or blocked).
- `unsorted` high → run `VACUUM SORT ONLY` (auto vacuum usually handles it) (gated: unconfirmed, source is paywalled or blocked).
- `stats_off` high → `ANALYZE` (gated: unconfirmed, source is paywalled or blocked).
In `EXPLAIN`, join steps labelled `DS_DIST_NONE` / `DS_DIST_ALL_NONE` are co-located; `DS_BCAST_INNER` / `DS_DIST_BOTH` mean data movement at query time (gated: unconfirmed, source is paywalled or blocked) — the signal to revisit keys.

## 4. Change safely
```sql
ALTER TABLE sales.fact_orders ALTER DISTSTYLE KEY DISTKEY customer_id;
ALTER TABLE sales.fact_orders ALTER SORTKEY (order_date, customer_id);
ALTER TABLE sales.fact_orders ALTER DISTSTYLE AUTO;
```
These redistribute/re-sort the table (the ALTER syntax (gated: unconfirmed, source is paywalled or blocked)) — schedule on large tables. The docs point to `SVV_ALTER_TABLE_RECOMMENDATIONS` for current recommendations and `SVL_AUTO_WORKER_ACTION` for actions automatic table optimization already took.

## 5. Serverless and RA3
AUTO is the default when no distribution style is given; check the Redshift docs for how distribution and sort keys apply on RA3 and Redshift Serverless.

## Verify
- [ ] Top 10 tables by size have `skew_rows` below ~4.
- [ ] Key joins in the busiest queries show `DS_DIST_NONE` or `DS_DIST_ALL_NONE`.
- [ ] Date-filtered queries scan fewer blocks after setting the sort key (`SVL_QUERY_SUMMARY` / `SYS_QUERY_DETAIL`).

## Checked

- Date: 2026-11-02.
- Confirmed against: Redshift Developer Guide pages on choosing distribution and sort keys, distributing data (AUTO default, EVEN round-robin and not for joined tables, KEY co-location, ALL copy on every node with multiplied storage, SVL_AUTO_WORKER_ACTION, SVV_ALTER_TABLE_RECOMMENDATIONS) and SVV_TABLE_INFO (diststyle values incl. AUTO(ALL)/AUTO(EVEN)/AUTO(KEY), sortkey1, skew_rows definition).
- Removed: the Serverless/RA3 statement.
- Gated: the 1 MB zone-map size, interleaved-key remarks, skew cut-off, unsorted/stats_off guidance, DS_* join labels and ALTER syntax (not stated in the fetched pages).

Method: documentation only; no commands were run.
