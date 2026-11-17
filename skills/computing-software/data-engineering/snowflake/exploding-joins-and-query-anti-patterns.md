---
id: computing-software.data-engineering.snowflake.exploding-joins-and-query-anti-patterns
name: exploding-joins-and-query-anti-patterns
category: computing-software
field: data-engineering
product: snowflake
tags: [snowflake, exploding-joins, query-profile, union-vs-union-all, order-by-limit, row-explosion, snowflake-performance, sql-anti-patterns]
level: practitioner
status: docs-checked
description: "Spot and fix common Snowflake query problems in the Query Profile: exploding joins, UNION vs UNION ALL, non-equality joins, spilling and weak pruning."
sources:
  - https://docs.snowflake.com/en/user-guide/ui-snowsight-activity
  - https://docs.snowflake.com/en/user-guide/querying-joins
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Exploding joins and query anti-patterns

**Goal:** spot in the query profile the classic shapes that waste compute and fix them in SQL.

## Exploding joins
Profile signal: the Join operator produces significantly (often by orders of magnitude) more tuples than it consumes.
Causes named in the Snowflake docs:
- Joining tables without a join condition (a Cartesian product).
- A condition where records from one table match multiple records from another.
In practice that means a join key that is not unique on the side you assumed (a dimension with duplicate keys, an SCD2 table joined without a date range), a missing join column, or a many-to-many join between two facts.
Fix:
```sql
-- check uniqueness before joining
select customer_id, count(*) from dim_customer group by 1 having count(*) > 1 limit 10;
-- aggregate before joining facts
with p as (select order_id, sum(amount) paid from payments group by 1)
select o.*, p.paid from orders o left join p using (order_id);
```

## UNION vs UNION ALL
`UNION ALL` concatenates the inputs; `UNION` also performs duplicate elimination. A common mistake is using `UNION` when `UNION ALL` semantics are enough. In Query Profile it shows as a UnionAll operator with an extra Aggregate operator on top. Use `UNION ALL` unless duplicates must be removed.

## Non-equality joins
The profile lists an Equality Join Condition and an Additional Join Condition. Non-equality join predicates (`on a.ts between b.start and b.end`) can result in significantly slower processing and should be avoided if possible; add an equality key (for example a customer id) or bucket by date first.

## Spilling
When memory is insufficient for an operation (for example duplicate elimination on a huge data set), data spills to local disk and then to remote storage, which can have a profound effect on performance. The profile reports bytes spilled to local and remote storage. Reducing the rows an operator must hold (aggregate first, fix an exploding join) is the first remedy; consult the docs for the full list of recommendations.

## Inefficient pruning
Compare Partitions scanned with Partitions total in the TableScan operator. If the former is a small fraction of the latter, pruning is efficient. If not, and a Filter operator above TableScan discards many rows, a different data organisation (for example a clustering key on a very large table) may help that query.

## Verify
- [ ] Query profile after the fix: join output rows are close to the expected count, and there is no remote spill.
- [ ] Partitions scanned dropped relative to Partitions total where pruning was the problem.

## Checked
2026-11-09. Confirmed against the Snowflake docs "Monitor queries and view the Query Profile" (exploding joins, UNION without ALL, inefficient pruning, spilling, non-equality join predicates) and "Working with joins" (join basics). Removed as unconfirmed on those pages: functions on filter columns and pruning behaviour, giant IN lists, needless ORDER BY, SELECT * byte ratios, and repeated CTE evaluation.
Method: documentation only; no commands were run.
