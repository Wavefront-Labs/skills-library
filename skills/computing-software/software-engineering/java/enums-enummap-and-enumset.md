---
id: computing-software.software-engineering.java.enums-enummap-and-enumset
name: enums-enummap-and-enumset
category: computing-software
field: software-engineering
product: java
tags: [java, java-enums, enummap, enumset, enum-switch, constant-specific-methods, modern-java]
level: practitioner
status: docs-checked
description: "Use Java enums fully: fields and constant-specific methods, valueOf safety, exhaustive switch, EnumMap and EnumSet instead of ordinal tricks, and persistence pitfalls."
sources: ["https://docs.oracle.com/javase/specs/jls/se21/html/jls-8.html#jls-8.9", "https://dev.java/learn/classes-objects/enums/", "https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/EnumMap.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Enums, EnumMap and EnumSet

**Goal:** type-safe fixed sets of values carrying behaviour, with the fast specialised
collections built for them.

## Enums with data and behaviour
```java
public enum Plan {
    FREE(0, 1) {
        @Override boolean canExport() { return false; }
    },
    PRO(20, 10),
    TEAM(50, 100);

    private final int priceUsd;
    private final int seats;
    Plan(int priceUsd, int seats) { this.priceUsd = priceUsd; this.seats = seats; }
    boolean canExport() { return true; }        // constant-specific override above
    public int seats() { return seats; }
}
```
Enums have one instance per constant, so compare constants with `==`.

## Parsing safely
```java
Plan.valueOf("PRO");              // IllegalArgumentException on unknown, NPE on null
static Optional<Plan> parse(String s) {
    return Arrays.stream(Plan.values()).filter(p -> p.name().equalsIgnoreCase(s)).findFirst();
}
```
For external codes different from names, keep a static `Map<String, Plan>` built in a static
initializer.


## EnumSet and EnumMap
```java
EnumSet<Permission> perms = EnumSet.of(Permission.READ, Permission.WRITE);
EnumSet<Permission> none = EnumSet.noneOf(Permission.class);
EnumSet.range(Day.MONDAY, Day.FRIDAY);
EnumMap<Plan, BigDecimal> revenue = new EnumMap<>(Plan.class);
```
`EnumSet` is represented as bit vectors and `EnumMap` as arrays (per their Javadoc): compact and fast,
iteration in declaration order. Replace `int` bit flags with `EnumSet` and ordinal-indexed arrays
with `EnumMap`.

## Persistence pitfalls
- Never persist `ordinal()`: reordering or inserting constants corrupts data. Persist a stable name or code (check your persistence library's enum-mapping options).
- Renaming a constant breaks stored names; keep a stable `code` field for data.
- For JSON, map enums by a stable code and decide how unknown values are handled (see your JSON library's docs).

## Verify
- [ ] No `ordinal()` in persistence or wire formats.

## Checked

- Date: 2026-10-28
- Confirmed in the Java SE 21 Javadoc (EnumSet, EnumMap, Enum pages): EnumSet bit vectors, EnumMap arrays, natural (declaration) order, Enum.valueOf throws IllegalArgumentException for an unknown name.
- Removed: Effective Java item numbers, JPA and Jackson specifics, exhaustive switch section (JLS 15.28 not fetched), values() clone remark.
Method: documentation only; no commands were run.
