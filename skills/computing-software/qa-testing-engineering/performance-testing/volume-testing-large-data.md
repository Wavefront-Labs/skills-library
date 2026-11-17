---
id: computing-software.qa-testing-engineering.performance-testing.volume-testing-large-data
name: volume-testing-large-data
category: computing-software
field: qa-testing-engineering
product: performance-testing
tags: [volume-testing, large-data-sets, performance-testing, database-growth, data-volume]
level: practitioner
status: draft
description: "Run volume tests with production-scale data: generate realistic volumes and skew, test queries, reports, batch jobs and pagination, and project future growth."
sources:
  - https://www.istqb.org/certifications/performance-tester
  - https://www.postgresql.org/docs/current/using-explain.html
  - https://www.postgresql.org/docs/current/functions-srf.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Volume testing with large data sets

**Goal:** confirm the system performs with the data volumes it will hold (today and in 1-3 years), not the few hundred rows in test environments. ISTQB Performance Tester lists volume testing as a distinct type.

## Plan volumes
- Current production counts per key table and growth rate; target = today x growth over the planning horizon.
- Realistic distribution: heavy users (one customer with 100k orders), skewed popularity, long text fields, many versions/history rows.

## Generate data
```sql
-- Postgres: 50M orders with skew toward recent dates and a few heavy customers
INSERT INTO orders (customer_id, created_at, total)
SELECT CASE WHEN random() < 0.1 THEN (random()*100)::int + 1 ELSE (random()*2000000)::int + 1 END,
       now() - (random()^3) * interval '1095 days',
       round((random()*200)::numeric, 2)
FROM generate_series(1, 50000000);
ANALYZE orders;
```
Or masked production snapshots; or Faker for text-heavy tables. Load with `COPY`, then rebuild indexes and `ANALYZE`.

## What to test
- Search, list and filter endpoints (pagination with OFFSET degrades at large offsets; keyset pagination does not).
- Reports and exports (memory use, timeouts, file sizes).
- Batch jobs and migrations (run time vs maintenance window).
- Backup/restore and index rebuild times.
- UI with huge collections (rendering 10k rows, virtual scrolling).
- Heavy-user accounts specifically.

## Measure
- Response times per operation at volume vs at small volume (same low concurrency, to isolate data effects from load effects).
- Query plans: `EXPLAIN (ANALYZE, BUFFERS)` for slow queries, look for seq scans, sorts spilling to disk.
- Storage growth and index sizes.

## Gotchas
- Uniform random data hides hot-spot problems; model skew.
- Statistics not updated after bulk load give misleading plans.
- Volume and load are different questions; combine only after each is understood.

## Verify
Key operations meet their targets at projected volume, heavy-user scenarios are covered, and query plans are reviewed for the slowest operations.
