---
id: computing-software.qa-testing-engineering.performance-testing.lock-contention-concurrency-testing
name: lock-contention-concurrency-testing
category: computing-software
field: qa-testing-engineering
product: performance-testing
tags: [lock-contention-testing, concurrency-testing, hot-row-contention, race-under-load]
level: practitioner
status: draft
description: "Test concurrency under load: many users on the same records, DB lock waits and deadlocks, optimistic locking conflicts, pool contention and oversell races."
sources:
  - https://www.postgresql.org/docs/current/explicit-locking.html
  - https://www.postgresql.org/docs/current/monitoring-stats.html
  - https://dev.mysql.com/doc/refman/8.0/en/innodb-deadlocks.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Concurrency testing for contention and locking

**Goal:** find failures that only appear when many requests touch the same resource simultaneously: oversold stock, duplicate charges, deadlocks, lock waits that collapse throughput.

## Design
- **Hot-spot scenario:** all VUs operate on a small set of records (one product with stock 100, one account balance). Contrast with a spread-out scenario on many records.
- **Synchronised bursts:** k6 `per-vu-iterations` with all VUs starting together, or a barrier (wait until a fixed timestamp) to maximise overlap.
- Mix reads and writes in production ratios plus a write-heavy variant.

```js
// 200 VUs try to buy the last 100 units at once
export const options = { scenarios: { race: { executor: 'per-vu-iterations', vus: 200, iterations: 1, maxDuration: '1m' } } };
export default function () {
  const r = http.post(`${BASE}/orders`, JSON.stringify({ sku: 'HOT-1', qty: 1 }), { headers });
  check(r, { 'created or sold out': (x) => x.status === 201 || x.status === 409 });
}
// teardown: assert exactly 100 orders exist and stock == 0 (never negative)
```

## Invariants to check after the run
Stock never negative; sum of balances conserved; no duplicate orders per idempotency key; every accepted request persisted.

## Database signals (PostgreSQL)
```sql
SELECT pid, wait_event_type, wait_event, state, query FROM pg_stat_activity WHERE wait_event_type = 'Lock';
SELECT deadlocks FROM pg_stat_database WHERE datname = current_database();
```
`log_lock_waits = on` with `deadlock_timeout` to log long waits. MySQL: `SHOW ENGINE INNODB STATUS` (LATEST DETECTED DEADLOCK), `performance_schema.data_lock_waits`.

## Application signals
Optimistic-lock exceptions / 409 rates, retry counts, connection pool wait time (HikariCP `pending` threads), thread pool saturation.

## Gotchas
- Spread-out data hides contention; realistic tests need realistic hot spots (popular items, shared counters).
- Retries on conflict can amplify load: measure attempts per success.

## Verify
Invariant checks pass at high concurrency; lock wait time and deadlock counters stay within agreed limits.
