---
id: computing-software.data-engineering.apache-spark.join-hints-and-bucketing
name: join-hints-and-bucketing
category: computing-software
field: data-engineering
product: apache-spark
tags: [apache-spark, spark, spark-sql, join-hints, broadcast-join, sort-merge-join, shuffle-hash-join, bucketing, bucketby, sortmergejoin, cross-join, explain-plan, catalyst-optimizer, pyspark]
level: advanced
status: docs-checked
description: "Force the right Spark join strategy with hints and eliminate shuffle entirely with bucketing, when AQE's defaults aren't enough."
sources:
  - https://spark.apache.org/docs/latest/sql-ref-syntax-qry-select-hints.html#join-hints
  - https://spark.apache.org/docs/latest/sql-data-sources-load-save-functions.html#bucketing-sorting-and-partitioning
  - https://spark.apache.org/docs/latest/sql-performance-tuning.html#join-strategy-hints-for-sql-queries
  - https://github.com/apache/spark/blob/master/sql/catalyst/src/main/scala/org/apache/spark/sql/internal/SQLConf.scala
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Join hints and bucketing — overriding Catalyst when it guesses wrong

**Goal:** when AQE's runtime size estimates still pick the wrong join strategy, or a repeated join keeps re-shuffling the same large tables, force the plan or eliminate the shuffle structurally. Complements computing-software.data-engineering.apache-spark.shuffle-and-skew-tuning, which covers reading the UI and fixing skew — this skill covers steering which join algorithm actually runs and avoiding the shuffle up front.

## 1. The four join strategies and when each applies
- **BroadcastHashJoin**: one side is sent whole to every executor — no shuffle on the large side (broadcast nested loop join is used when there is no equi-join key). See `shuffle-and-skew-tuning` for the size threshold.
- **SortMergeJoin** (default for large-large equi-joins): both sides shuffled and sorted on the join key, then merged. Reliable, but pays a shuffle on both sides every time the query runs if the data isn't already co-partitioned.
- **ShuffleHashJoin**: builds a hash table from one side after shuffle instead of sorting — can beat sort-merge when one side is markedly smaller but still too big to broadcast, at the cost of holding that side's partition in memory per task (OOM risk if the "smaller" side is skewed).
- **BroadcastNestedLoopJoin / CartesianProduct**: used for non-equi joins (`<`, `>`, range conditions) or accidental cross joins. These scale catastrophically (`O(n×m)`) — if `EXPLAIN` shows one of these where an equi-join was intended, the join condition is almost certainly wrong (e.g. mismatched column names producing an implicit cross join), not a performance tuning problem.

## 2. Forcing a strategy with hints
```sql
SELECT /*+ BROADCAST(dim) */ * FROM fact JOIN dim ON fact.id = dim.id;
SELECT /*+ MERGE(a) */ * FROM a JOIN b ON a.k = b.k;           -- shuffle sort merge (aliases SHUFFLE_MERGE, MERGEJOIN)
SELECT /*+ SHUFFLE_HASH(b) */ * FROM a JOIN b ON a.k = b.k;    -- suggest shuffle hash join
SELECT /*+ SHUFFLE_REPLICATE_NL(b) */ * FROM a JOIN b ON a.k = b.k;  -- suggest shuffle-and-replicate nested loop join
```
Same via the DataFrame API: `df.hint("broadcast")`, `df.hint("merge")`, etc. Hints are suggestions: Spark is not guaranteed to follow one because a strategy may not support every join type. When hints on both sides conflict, the priority is BROADCAST, then MERGE, then SHUFFLE_HASH, then SHUFFLE_REPLICATE_NL. `BROADCAST` (aliases `BROADCASTJOIN`, `MAPJOIN`) applies regardless of `autoBroadcastJoinThreshold`. Use hints when `ANALYZE TABLE` statistics are stale/missing and AQE's runtime correction (which only kicks in after the first shuffle exchange produces real sizes) still isn't enough, e.g. when you know a "large" table is actually small after an early filter that the optimizer doesn't push down accurately.
- **Gotcha:** a bad hint can make things worse — forcing `BROADCAST` on a table that's actually large causes a driver/executor OOM with a confusing stack trace far from the hint itself. Verify the table's size before forcing.

## 3. Bucketing — avoid the shuffle on every run, not just this query
`df.write.bucketBy(8, "user_id").sortBy("user_id").saveAsTable("fact_bucketed")` (bucketing and sorting apply only to persistent tables) pre-partitions and pre-sorts data on disk by the join key. If two tables are bucketed identically (same column, same bucket count) on the key they're joined on, Spark skips the shuffle+sort step entirely on every subsequent join — the cost is paid once at write time instead of on every query.
- Only pays off for **repeated joins on the same key** between large tables (e.g. a daily job joining the same fact/dimension pair) — a one-off join doesn't justify the write-time cost.
- **Gotcha:** with equal bucket counts the shuffle is skipped. With different counts, `spark.sql.bucketing.coalesceBucketsInJoin.enabled` (default false) lets Spark coalesce the larger side when one count divides the other, for sort-merge and shuffled hash joins; otherwise, or when a side is not bucketed, Spark shuffles as normal. Check `EXPLAIN` for the absence of an `Exchange` below the join. `spark.sql.sources.bucketing.enabled` (default true) set to false treats bucketed tables as normal tables.

## Verify
- [ ] `EXPLAIN` (or `EXPLAIN FORMATTED`) on the real query shows the intended join type — not a `CartesianProduct` from a malformed condition.
- [ ] Any forced `BROADCAST` hint's target table size was checked (`count()`/stats), not assumed.
- [ ] A bucketed join's plan has no `Exchange` node between the scan and the join — confirming the shuffle was actually skipped, not silently reintroduced.
- [ ] Bucket column and count match on both sides (or the coalesce setting applies) for a join expected to skip shuffle.

## Checked
Checked 2026-10-25 against the Apache Spark documentation sources (apache/spark docs/ and SQLConf.scala on master, last commit 2026-10-24; docs site: spark.apache.org/docs/latest).
Confirmed in sql-ref-syntax-qry-select-hints.md: hint names and aliases, priority order, hints not guaranteed, BROADCAST ignores the threshold; SHUFFLE_REPLICATE_NL is shuffle-and-replicate nested loop join (not broadcast nested loop; previous example also used a non-equi condition). Confirmed in SQLConf.scala: bucketing.coalesceBucketsInJoin.enabled default false and its divisibility rule, sources.bucketing.enabled default true. Confirmed in load-save docs that bucketBy and sortBy apply to persistent tables. Wrong claim fixed: bucket counts need not match exactly.

Method: documentation only; no commands were run.
