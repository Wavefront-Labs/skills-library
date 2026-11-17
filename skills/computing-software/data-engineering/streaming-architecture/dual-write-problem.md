---
id: computing-software.data-engineering.streaming-architecture.dual-write-problem
name: dual-write-problem
category: computing-software
field: data-engineering
product: streaming-architecture
tags: [streaming-architecture, dual-write-problem, transactional-outbox, cdc, delivery-semantics, consistency, event-driven]
level: advanced
status: draft
description: "Avoid the dual-write problem when a service updates its database and publishes events: why it loses or invents events, and outbox, CDC and listen-to-yourself fixes."
sources:
  - https://microservices.io/patterns/data/transactional-outbox.html
  - https://debezium.io/documentation/reference/stable/transformations/outbox-event-router.html
  - https://www.confluent.io/blog/dual-write-problem/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# The dual-write problem

**Goal:** the database state and the event stream never disagree, even when the service crashes between steps.

## The bug
```python
db.execute("update orders set status='PAID' where id=%s", oid)
db.commit()
producer.send("order-events", {"id": oid, "status": "PAID"})   # crash here -> DB says PAID, no event
```
Reversing the order (publish, then commit) is worse: event published for a change that may roll back. Wrapping both in a "try/except and retry" still fails on process crashes. Two independent systems cannot be committed atomically without a coordinator (XA/2PC, which Kafka does not support).

Symptoms downstream: missing orders in the warehouse, consumers acting on states that never persisted, nightly reconciliation diffs.

## Fix 1: transactional outbox
Write the event into an `outbox` table **in the same DB transaction** as the state change; a relay publishes it.
```sql
begin;
update orders set status = 'PAID' where id = 42;
insert into outbox (id, aggregate_type, aggregate_id, type, payload, created_at)
values (gen_random_uuid(), 'order', '42', 'OrderPaid', '{"id":42,"status":"PAID"}', now());
commit;
```
Relay options: Debezium CDC on the outbox table with the **Outbox Event Router** SMT (routes by `aggregate_type` to topics, keys by `aggregate_id`), or a polling publisher (`select ... for update skip locked`, publish, mark sent). Delivery is at least once: consumers dedupe on the outbox `id`.

## Fix 2: CDC on the business tables
Skip events in application code; stream table changes with Debezium/DMS. Simple and complete, but events are row-level ("orders row changed"), coupling consumers to the internal schema. Good for analytics replication; for domain events prefer the outbox.

## Fix 3: event first, state from the log (listen to yourself)
Service publishes the event to Kafka only; its own consumer updates the DB from the topic (event sourcing style). The log is the source of truth; DB is a projection. Read-your-writes needs care.

## Choosing
| Need | Pattern |
|---|---|
| Domain events for other services | outbox + CDC relay |
| Replicate tables to lake/warehouse | CDC on tables |
| Log as system of record | event sourcing / listen to yourself |

## Gotchas
- Outbox table growth: delete published rows (Debezium reads from the WAL, so you can delete immediately after insert in the same transaction; the insert is still captured).
- Ordering: key events by aggregate id so per-entity order holds in the topic.
- Do not publish inside DB triggers calling external systems; same dual-write in disguise.

## Verify
- [ ] Kill the service between DB commit and publish in a test: event still appears (outbox) exactly once after dedup.
- [ ] Reconciliation of DB state vs projected state from the topic shows zero diffs.
