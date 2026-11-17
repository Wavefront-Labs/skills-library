---
id: computing-software.software-engineering.java.records-and-compact-constructors
name: records-and-compact-constructors
category: computing-software
field: software-engineering
product: java
tags: [java, java-records, modern-java, compact-constructor, immutability, value-objects, dto, jackson-records, jpa-records, java-data-modeling]
level: practitioner
status: docs-checked
description: "Use Java records for immutable data carriers: compact-constructor validation, defensive copies, custom accessors, and where records don't fit (JPA entities)."
sources: ["https://openjdk.org/jeps/395", "https://docs.oracle.com/javase/specs/jls/se21/html/jls-8.html#jls-8.10"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Records and compact constructors

**Goal:** replace boilerplate DTOs and value objects with records (Java 16+) while
keeping invariants and immutability real.

## Basics
```java
public record Money(BigDecimal amount, Currency currency) {
    public Money {                                   // compact canonical constructor
        Objects.requireNonNull(amount, "amount");
        Objects.requireNonNull(currency, "currency");
        if (amount.scale() > currency.getDefaultFractionDigits())
            throw new IllegalArgumentException("too many decimals: " + amount);
        amount = amount.stripTrailingZeros();         // reassign PARAMETER; field set after
    }
    public Money plus(Money o) { check(o); return new Money(amount.add(o.amount), currency); }
    public static Money zero(Currency c) { return new Money(BigDecimal.ZERO, c); }
}
```
The compiler generates private final fields, accessors `amount()` (no `get` prefix),
`equals`/`hashCode`/`toString` over all components.

## Shallow immutability: copy collections
```java
public record Order(String id, List<Line> lines) {
    public Order { lines = List.copyOf(lines); }      // defensive, unmodifiable, rejects nulls
}
```
Without this the caller can mutate the list after construction, and `equals`/`hashCode`
change under you (broken HashMap keys). Arrays as components compare by identity in
`equals`; avoid them or override equals/hashCode.

## What records can and can't do
- Can: implement interfaces, have static fields/methods, instance methods, nested
  types, be generic, be local (declared inside a method).
- Can't: extend a class (implicitly `final`, extend `Record`), declare instance fields
  beyond components, have setters.
- Overriding an accessor is allowed, but it must keep the component semantics.

## Framework fit
Check each framework's own documentation for record support (JSON mappers, configuration binding, JPA
providers); records are immutable and have no no-arg constructor, which many entity mappers expect.

## Pattern matching
Records deconstruct in patterns (Java 21):
`if (shape instanceof Circle(var center, var r)) { ... }`.
See computing-software.software-engineering.java.sealed-types-and-pattern-matching.

## Checked
2026-10-28: Confirmed in JEP 395 and JLS 8.10: record components, canonical and compact constructors, records are implicitly final and cannot extend a class. Removed library version numbers and JPA/Jackson/Spring/Hibernate claims that were not in fetched pages, and the dev.java source (stub).
Method: documentation only; no commands were run.

## Verify
- [ ] Constructing with invalid data throws in tests.
- [ ] Mutating the source list after construction does not change the record.
- [ ] No record holds mutable arrays or exposes internal mutable state.
