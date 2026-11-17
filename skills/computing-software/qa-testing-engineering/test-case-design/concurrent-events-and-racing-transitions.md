---
id: computing-software.qa-testing-engineering.test-case-design.concurrent-events-and-racing-transitions
name: concurrent-events-and-racing-transitions
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [concurrent-transitions, state-transition-testing, race-conditions, optimistic-locking, concurrency-testing]
level: practitioner
status: verified
description: "Test concurrent events on a state machine: two actors racing on one entity, duplicate events, optimistic locking and out-of-order message delivery."
sources:
  - https://www.istqb.org/certifications/certified-tester-foundation-level
  - https://www.postgresql.org/docs/current/explicit-locking.html
  - https://martinfowler.com/eaaCatalog/optimisticOfflineLock.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Concurrent events and racing transitions

**Goal:** find the defects that appear only when two events hit the same state at nearly the same time.

## Typical races
| Scenario | Risk |
|---|---|
| Customer cancels while warehouse ships | order both Cancelled and Shipped; refund and shipment both happen |
| Double click / retry on Pay | two charges |
| Two approvers approve simultaneously | duplicate payments or skipped second-level approval |
| Message queue delivers "Shipped" before "Paid" | invalid transition rejected or state corrupted |
| Timer fires as user acts (auto-cancel vs pay) | paid order cancelled |

## Test techniques
1. **Barrier-synchronised API calls:** fire N identical or conflicting requests at once and assert exactly one wins.
```python
import asyncio, httpx
async def race():
    async with httpx.AsyncClient(base_url=BASE) as c:
        r = await asyncio.gather(c.post(f"/orders/{oid}/cancel"), c.post(f"/orders/{oid}/ship"))
    codes = sorted(x.status_code for x in r)
    assert codes == [200, 409]          # one wins, the other gets a conflict
```
Repeat the race hundreds of times; races are probabilistic. Run against a threaded stdlib server over SQLite, a read-then-write handler returned `[200, 200]` in 30 of 30 races, and the conditional `UPDATE ... WHERE status IN (...)` handler returned `[200, 409]` in 30 of 30.
2. **Deterministic interleaving:** inject a pause hook between read and write in the service (test-only), start request A, then B, then release A.
3. **Out-of-order and duplicate events:** publish consumer messages in shuffled order and twice; assert final state and side effects once.
4. **Timer vs user action:** set the clock to the expiry instant and trigger both.

## What the system should do
Optimistic locking (`version` column, `UPDATE ... WHERE id = ? AND version = ?`, 409 on mismatch), or row locks (`SELECT ... FOR UPDATE`), conditional transitions (`UPDATE orders SET status='Cancelled' WHERE id=? AND status IN ('Created','Paid')` and check rows affected), idempotency keys for retries.

## Gotchas
- Tests against a single-threaded local server may never interleave; run against a multi-worker deployment.
- Assert on persisted state and side effects (payments, emails), not only on HTTP responses.

## Verify
For each high-risk conflicting event pair, a repeated race test shows exactly one effective transition and no duplicated side effects.
