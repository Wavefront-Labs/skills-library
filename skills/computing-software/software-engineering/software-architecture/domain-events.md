---
id: computing-software.software-engineering.software-architecture.domain-events
name: domain-events
category: computing-software
field: software-engineering
product: software-architecture
tags: [software-architecture, domain-driven-design, ddd, domain-events, integration-events, eventual-consistency, event-driven-architecture]
level: practitioner
status: draft
description: "Model and publish domain events: naming in past tense, payload design, raising inside aggregates, dispatching after commit, domain vs integration events and versioning."
sources:
  - https://martinfowler.com/eaaDev/DomainEvent.html
  - https://learn.microsoft.com/en-us/dotnet/architecture/microservices/microservice-ddd-cqrs-patterns/domain-events-design-implementation
  - https://www.dddcommunity.org/library/vernon_2011/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Domain events

A domain event records something that happened in the domain that domain experts care about: `OrderPlaced`, `PaymentFailed`, `SeatReserved`.

## Naming and content
- Past tense, business language (from event storming): `OrderShipped`, not `UpdateOrderStatus` or `OrderStatusChanged` (too generic).
- Immutable; include event id, occurred-at timestamp, aggregate id, aggregate version, and the facts consumers need.
- Payload size: **thin** (ids only, consumers call back for data - creates coupling and load) vs **fat** (state needed by consumers - more schema to evolve). Prefer enough data that common consumers need no callback.

## Raising and dispatching
1. The aggregate records events in an internal list when its state changes (`self.events.append(OrderPlaced(...))`).
2. The application service saves the aggregate.
3. Events are dispatched **after the transaction commits** - never before (a rolled-back transaction must not have told the world). Options:
   - In-process: dispatcher in the unit of work's post-commit hook (EF Core `SaveChanges` override, Spring `@TransactionalEventListener(phase = AFTER_COMMIT)`).
   - Cross-process: write events to an outbox table in the same transaction, relay to the broker (transactional outbox skill).
4. Clear the aggregate's event list once dispatched.

## Domain events vs integration events
| | Domain event | Integration event |
|---|---|---|
| Scope | inside one bounded context | published to other contexts/services |
| Contract | can change with the model | public contract: versioned, documented (AsyncAPI, schema registry) |
| Transport | in-memory | broker (Kafka, RabbitMQ, SNS/SQS, EventBridge) |
Map domain events to integration events deliberately; do not publish internal model changes directly.

## Consumer rules
- At-least-once delivery: handlers are idempotent (dedupe on event id).
- Ordering is guaranteed only per partition/key (Kafka key = aggregate id); handlers tolerate out-of-order or use the aggregate version.
- Versioning: additive changes only; new event type or version field for breaking changes; upcasters for stored events.

## Verify
- [ ] Aggregate tests assert the events raised by each command.
- [ ] Failing transaction test shows no event published.
- [ ] Replaying the same event twice leaves consumer state unchanged.
