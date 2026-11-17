---
id: computing-software.data-engineering.streaming-architecture.event-sourcing-and-cqrs
name: event-sourcing-and-cqrs
category: computing-software
field: data-engineering
product: streaming-architecture
tags: [streaming-architecture, event-sourcing, cqrs, projections, event-store, snapshots, read-models, kafka]
level: advanced
status: draft
description: "Apply event sourcing and CQRS: events as the system of record, projections into read models, snapshots, versioning events, and what it means for analytics pipelines."
sources:
  - https://martinfowler.com/eaaDev/EventSourcing.html
  - https://martinfowler.com/bliki/CQRS.html
  - https://learn.microsoft.com/en-us/azure/architecture/patterns/event-sourcing
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Event sourcing and CQRS

**Goal:** know when storing every state change as an immutable event (and deriving current state) is worth it, and how to run the read side and analytics on top.

## Concepts
- **Event sourcing:** the system of record is an append-only sequence of domain events per aggregate (`OrderPlaced`, `ItemAdded`, `OrderPaid`). Current state = fold over events.
- **CQRS:** separate write model (commands validated against aggregate state, producing events) from read models (projections optimised per query).
They combine well but are independent: CQRS without event sourcing (separate read replicas/views) is common.

## Event store choices
- Purpose-built (EventStoreDB/Kurrent): per-stream optimistic concurrency (`expectedVersion`), subscriptions.
- Relational table `events(stream_id, version, type, payload, metadata, created_at, primary key(stream_id, version))`: unique constraint gives optimistic concurrency; outbox/CDC to publish.
- Kafka alone is a weak primary event store: no per-key optimistic concurrency check, and reading one aggregate's events means scanning a partition. Common pattern: DB event store + Kafka for distribution.

## Projections
```python
def project(event, read_db):
    if event.type == "OrderPlaced":
        read_db.upsert("orders_view", {"id": event.order_id, "status": "PLACED", "total": 0})
    elif event.type == "ItemAdded":
        read_db.execute("update orders_view set total = total + %s where id = %s", (event.price, event.order_id))
    read_db.set_checkpoint("orders_view", event.global_position)   # same transaction as the update
```
- Store the projection checkpoint with the read model atomically (exactly-once effect).
- Rebuild a projection by replaying from position 0 into a new table, then switch.
- Read models are eventually consistent; UIs need read-your-writes strategies (return the new version, wait for checkpoint >= version).

## Snapshots
For long-lived aggregates, persist a snapshot every N events; load = snapshot + events after it. Snapshots are a cache: always rebuildable.

## Event versioning
Events are forever. Evolve with additive fields, **upcasters** (transform old event versions to the new shape on read), or new event types. Never rewrite history except for legal erasure (crypto-shredding: encrypt PII per subject, delete the key).

## Analytics on event-sourced systems
- The event stream is a gift: full history of state changes, ideal for facts (accumulating snapshots, funnels).
- Land events raw (bronze) with stream id, version, global position; build state tables via SQL window functions or reuse projections.
- Domain events are a public contract: version and document them (schema registry).

## When not to use
Simple CRUD domains, teams new to the pattern, or when audit needs can be met by CDC + history tables. The operational complexity (projections, versioning, eventual consistency) is real.

## Verify
- [ ] Projection rebuild from scratch produces identical read model to the live one.
- [ ] Concurrency test: two commands on the same aggregate version, one rejected.
