---
id: computing-software.software-engineering.software-architecture.ddd-aggregates-and-invariants
name: ddd-aggregates-and-invariants
category: computing-software
field: software-engineering
product: software-architecture
tags: [software-architecture, domain-driven-design, ddd, aggregates, aggregate-root, invariants, consistency-boundary]
level: practitioner
status: verified
description: "Design DDD aggregates: pick consistency boundaries from invariants, keep them small, reference by id, one aggregate per transaction, and optimistic concurrency."
sources:
  - https://www.dddcommunity.org/library/vernon_2011/
  - https://martinfowler.com/bliki/DDD_Aggregate.html
  - https://learn.microsoft.com/en-us/dotnet/architecture/microservices/microservice-ddd-cqrs-patterns/microservice-domain-model
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Aggregates and invariants

An **aggregate** is a cluster of domain objects treated as a unit for data changes. The **aggregate root** is the only entry point; outside code holds references only to the root.

## Vernon's rules (Effective Aggregate Design)
1. **Model true invariants in consistency boundaries.** An invariant is a rule that must be true after every transaction ("order total equals sum of lines", "a seat cannot be booked twice"). Objects that share such a rule go in one aggregate.
2. **Design small aggregates.** Large aggregates (a `Customer` holding all orders) cause contention, slow loads, and lock conflicts. Most aggregates are a root plus a few value objects.
3. **Reference other aggregates by identity**, not object references: `order.customer_id`, not `order.customer`.
4. **Use eventual consistency outside the boundary.** Changes that span aggregates go through domain events and separate transactions.

## Shape
```python
class Order:                                   # aggregate root
    def __init__(self, order_id, customer_id):
        self.id, self.customer_id = order_id, customer_id
        self._lines: list[OrderLine] = []
        self.status = "open"
        self.version = 0                         # optimistic concurrency
        self.events = []
    def add_line(self, product_id, qty, price):
        if self.status != "open": raise DomainError("order closed")
        if qty <= 0: raise DomainError("qty must be positive")
        self._lines.append(OrderLine(product_id, qty, price))   # invariant enforced here only
    @property
    def total(self): return sum(l.qty * l.price for l in self._lines)
    def place(self):
        if not self._lines: raise DomainError("empty order")
        self.status = "placed"; self.events.append(OrderPlaced(self.id, self.total))
```
No public setters; mutations go through intention-revealing methods that check invariants.

## Persistence rules
- **One aggregate per transaction.** If a use case must change two aggregates atomically, revisit the boundary - or accept eventual consistency via events/outbox.
- Repositories exist per aggregate root (`OrderRepository`), load and save the whole aggregate.
- **Optimistic concurrency:** version column checked on save (`UPDATE ... WHERE id=? AND version=?`; JPA `@Version`, EF Core concurrency token). Retry or report conflict.

## Finding boundaries
Ask "what must be consistent immediately vs. within seconds?" Business people often accept eventual consistency ("inventory updated within a second of the order") once asked. Event storming surfaces the commands and invariants that suggest aggregates.

## Verify
- [ ] Unit tests on the root cover every invariant violation.
- [ ] No code outside the aggregate mutates its internal entities (encapsulated collections, architecture test).
- [ ] Concurrent update test produces a version conflict, not a lost update.
