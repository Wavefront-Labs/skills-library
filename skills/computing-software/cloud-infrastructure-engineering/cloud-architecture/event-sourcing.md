---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.event-sourcing
name: event-sourcing
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, data-patterns, event-sourcing, event-store, append-only, snapshots, optimistic-concurrency, event-upcasting, replay, audit-trail, eventstoredb, kafka]
level: advanced
status: docs-checked
description: "Store state as an append-only event stream per entity: event design, optimistic concurrency, snapshots, schema evolution by upcasting, crypto-shredding and idempotent consumers."
sources: ["https://learn.microsoft.com/azure/architecture/patterns/event-sourcing", "https://martinfowler.com/eaaDev/EventSourcing.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Event sourcing

The event store is the system of record; current state is derived by replaying an entity's eventstream (rehydration). Read-optimised materialized views are projections of it.

## When it pays
The Azure Architecture Center says to adopt it only when auditability and historical reconstruction justify the complexity: for most systems and most parts of a system, traditional data management is sufficient, and migrating to or from event sourcing is costly. Good fits: capturing intent in the data, minimising conflicting updates, replay and rollback, audit logs, decoupling input from downstream tasks, and CQRS with acceptable eventual consistency. Poor fits: plain CRUD without audit or replay needs, prototypes and short-lived systems, data needing real-time consistent views, mostly static reference data, and teams without event-driven experience. It can be applied selectively (a payment ledger yes, user profile management no).

## Build
1. **One eventstream per entity.** The entity that owns a stream is typically a DDD aggregate. Events are immutable and appended only.
2. **Design events for intent**, not resulting state: "two seats reserved" beats "remaining seats changed to 42".
3. **Optimistic concurrency**: the store rejects an append if the stream changed since it was read; the handler reloads, re-evaluates and retries. Conflicts that span several entities (stock reduced while an order arrives) still need business-level reconciliation such as a back order.
4. **Ordering**: a timestamp on each event helps, and a common practice is an incrementing identifier per entity so the store can reject a duplicate position.
5. **Event store options**: a purpose-built append-only database (built-in stream reads, optimistic concurrency, snapshots) or a relational or document table you build those behaviours on. Do not use a message broker such as Apache Kafka as the event store: it typically lacks per-entity stream queries and optimistic concurrency, though it works as a distribution layer to projections and external consumers.
6. **Snapshots** every N events when streams get long: load the latest snapshot and replay only later events. A snapshot is an optimisation, regenerable from the stream; balance snapshot storage against rehydration time.
7. **Projections** are materialized views, eventually consistent with the store. Events are typically low level, so generate separate integration events for other systems where needed.
8. **Consumers must be idempotent** (delivery is typically at least once): track the last processed sequence number per consumer, or make state changes safe to repeat. Watch for processing that raises new events in a loop.

## Schema evolution
Never update stored event data; reverse a change with a compensating event (a `ReservationCanceled` compensates `SeatsReserved`). Bugs that produced bad events leave them in the store, so replay may need compensating events or upcasters. Strategies from the page:
- tolerant deserialisation (ignore unknown fields, default missing ones) for additive changes;
- event versioning (version identifier in the envelope or type name);
- upcasting (chained transformations from old to current schema at read time, stored events unchanged);
- in-place migration, which breaks immutability and is a last resort.

## Personal data
Immutability conflicts with deletion laws. Either keep personal data outside the store and reference it by identifier, or crypto-shred: encrypt it with a per-subject key and delete the key. That adds encryption cost on every read and write and needs robust key management.

## Querying
There is no SQL-like query over events; you can read an entity's stream by identifier and replay it. Use projections for everything else.

## Testing
Given-when-then: set up past events, issue a command, assert on the new events. Also integration-test projections, idempotency and schema evolution paths.

## Verify
- [ ] Two concurrent commands on one stream: one wins, the other reloads and retries.
- [ ] A projection rebuilt from the full stream matches the live one.
- [ ] A duplicate event delivered twice changes the outcome once.
- [ ] Personal-data erasure path is tested before go-live.

## Checked
2026-11-08, documentation only.
Confirmed against: Azure Architecture Center, Event Sourcing pattern (last updated 2026-03-28), read in full.
Removed as unconfirmed by that page: the specific event envelope fields, the "every 100 events" example, named stores (EventStoreDB, Marten, DynamoDB, Cosmos DB), the "millions of events means the aggregate boundary is wrong" heuristic and the replay-mode advice for side effects.
Method: documentation only; no commands were run.
