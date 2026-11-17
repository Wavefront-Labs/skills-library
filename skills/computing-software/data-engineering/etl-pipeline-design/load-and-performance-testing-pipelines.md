---
id: computing-software.data-engineering.etl-pipeline-design.load-and-performance-testing-pipelines
name: load-and-performance-testing-pipelines
category: computing-software
field: data-engineering
product: etl-pipeline-design
tags: [etl-pipeline-design, pipeline-load-testing, performance-testing, scalability, capacity-planning]
level: advanced
status: draft
description: "Load-test data pipelines before volume grows: synthetic scaled datasets, measuring throughput and runtime curves, finding bottlenecks, and setting performance budgets."
sources:
  - https://docs.databricks.com/aws/en/optimizations/
  - https://docs.snowflake.com/en/user-guide/ui-query-profile
  - https://github.com/databrickslabs/dbldatagen
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Load and performance testing pipelines

**Goal:** know how runtime and cost scale with data volume, and fix bottlenecks before production hits them.

## Make test data at scale
- Scale real distributions, not uniform random data: skewed keys, realistic null rates, duplicate patterns.
- Tools: dbldatagen (Spark), Faker + numpy for generators, Snowflake `GENERATOR()` table function, TPC-DS/TPC-H data for engine baselines.
- Or clone production and replicate partitions (multiply by 2x, 5x, 10x with shifted dates/keys).
```sql
create table perf.orders_10x as
select o.* replace (o.order_id * 10 + g.n as order_id)
from core.orders o cross join (select seq4() n from table(generator(rowcount => 10))) g;  -- Snowflake
```

## Measure
- Runtime per step and total; throughput (rows/s, MB/s); cost (credits/DBUs per run).
- Run at 1x, 2x, 5x, 10x volumes: linear growth is fine; super-linear (sort/shuffle explosions, skew, exploding joins) is the risk.
- Streaming: sustained input rate vs processing rate, end-to-end latency percentiles, backlog recovery time after a pause.

## Find bottlenecks
- Query profiles / Spark UI: spill, skewed tasks, full scans without pruning, exploding joins.
- Source/sink limits: API rate limits, JDBC parallelism, warehouse concurrency.
- Small files / too many partitions.

## Performance budgets
Record "pipeline X: <= 45 min and <= N credits at 2x current volume" and re-run the test after major changes (or monthly) to catch regressions.

## Gotchas
- Warm caches distort results (result cache, disk cache): disable or run cold.
- Test environment compute must match production sizing.
- Testing only the happy path: also test backfill volume (30 days at once) and catch-up after outage.

## Verify
Runtime/cost vs volume chart for the pipeline exists, and the projected 12-month volume stays within the SLA on current compute.
