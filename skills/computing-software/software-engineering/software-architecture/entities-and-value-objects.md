---
id: computing-software.software-engineering.software-architecture.entities-and-value-objects
name: entities-and-value-objects
category: computing-software
field: software-engineering
product: software-architecture
tags: [software-architecture, ddd, entities-and-value-objects, value-objects, domain-modeling, immutability]
level: practitioner
status: verified
description: "Model DDD entities (identity, lifecycle) and value objects (immutable, equality by value, self-validating), and replace primitive fields with value objects."
sources: ["https://martinfowler.com/bliki/ValueObject.html", "https://www.domainlanguage.com/ddd/reference/", "https://learn.microsoft.com/en-us/dotnet/architecture/microservices/microservice-ddd-cqrs-patterns/implement-value-objects"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Entities and value objects

## Decide by asking "does identity matter?"
- **Entity**: continuity of identity over changing attributes. A Customer who changes name and
  address is the same customer. Equality = id.
- **Value object**: defined only by its attributes; interchangeable copies. Money(10, GBP), an
  Address, a DateRange, an EmailAddress. Equality = all attributes.
The same concept can be either in different contexts (an Address is a value in Ordering, an entity
in a postal-validation system).

## Value object rules
- Immutable: operations return new instances (`money.add(other)`).
- Self-validating in the constructor: an `EmailAddress` that exists is valid; no `isValid()`
  checks scattered around.
- Encapsulate behaviour: `DateRange.overlaps()`, `Money.allocate(ratios)` (handles rounding pennies).
- Language support: Java `record`, C# `record`/`readonly record struct`, Kotlin `data class` /
  `@JvmInline value class`, Python `@dataclass(frozen=True)`, TypeScript readonly classes or branded types.
```python
@dataclass(frozen=True)
class Money:
    amount: Decimal; currency: str
    def __post_init__(self):
        if not self.amount.is_finite() or self.amount.as_tuple().exponent < -2:
            raise ValueError("amount must be finite with at most 2 dp")   # NaN's exponent is a str: the old check raised TypeError
    def __add__(self, o):
        if o.currency != self.currency: raise ValueError("currency mismatch")
        return Money(self.amount + o.amount, self.currency)
```

## Entity rules
- Identity assigned early (UUID/ULID generated in the domain or a sequence); never use mutable
  business data (email) as identity.
- Keep entities lean: push attribute clusters and rules into value objects.
- State changes through intention-revealing methods (`order.ship(tracking)`), not setters.

## Persistence
Value objects map to embedded columns (JPA `@Embeddable`, EF Core owned types, `composite` in
SQLAlchemy) or JSON columns; collections of values to child tables without their own identity.

## Smell this fixes
Primitive obsession: `String currency, BigDecimal amount` pairs passed everywhere, validation
duplicated, units mixed.
