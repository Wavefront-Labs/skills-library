---
id: computing-software.software-engineering.software-architecture.cqrs
name: cqrs
category: computing-software
field: software-engineering
product: software-architecture
tags: [software-architecture, distributed-data, cqrs, read-models, projections, eventual-consistency, command-query-responsibility-segregation]
level: practitioner
status: verified
description: "Apply CQRS where it pays: separate command and query models, building read-model projections, handling eventual consistency in the UI, and when not to use it."
sources:
  - https://martinfowler.com/bliki/CQRS.html
  - https://learn.microsoft.com/en-us/azure/architecture/patterns/cqrs
  - https://www.eventstore.com/cqrs-pattern
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CQRS (Command Query Responsibility Segregation)

Use separate models for updating information (commands) and reading it (queries). Fowler's warning: for most systems CQRS adds risky complexity; use it for specific bounded contexts where read and write needs differ sharply.

## Levels
1. **Code-level split:** command handlers use the rich domain model; query handlers bypass it and run optimised SQL/views returning DTOs. Same database. Low cost, often enough.
2. **Separate read store:** writes go to the normalised write DB; projections update denormalised read models (Elasticsearch for search, Redis for counters, a document per screen). Read side scales independently.
3. **With event sourcing:** the write side stores events; projections build all read models from the event stream.

## Projections
```python
class OrderSummaryProjection:
    def handle(self, event):
        match event:
            case OrderPlaced(order_id=oid, customer_id=c, total=t):
                read_db.upsert("order_summary", oid, customer=c, total=t, status="placed")
            case OrderShipped(order_id=oid):
                read_db.update("order_summary", oid, status="shipped")
```
- Idempotent handlers: upserts alone are not enough. Run: replaying the old `OrderPlaced` after `OrderShipped` moved `status` back to `placed`, so track the last processed position/event version per projection and skip anything at or below it.
- Rebuildable: drop and replay from events or a full scan to fix bugs or add new read models.
- Monitor projection lag.

## Eventual consistency in the UI
After a command, the read model may not yet reflect it:
- Return the new state or version from the command and render it directly (optimistic UI).
- Read-your-writes: pass the command's resulting version and have the query wait/poll until the projection reaches it.
- Show "processing" states; avoid redirecting to a list that will not contain the new item yet.

## Use it when
- Read and write workloads differ by orders of magnitude or need different shapes (complex search vs simple transactional writes).
- Collaborative domains with complex invariants on writes and many screen-specific views.
- Already doing event sourcing.

## Do not use it when
- CRUD screens where reads and writes have the same shape.
- The team is not ready for eventual consistency bugs and extra infrastructure.

## Verify
- [ ] Projection rebuild from scratch produces the same read model as incremental processing.
- [ ] UI flow test covers the command-then-read path under projection lag.
