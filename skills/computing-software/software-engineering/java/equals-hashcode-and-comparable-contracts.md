---
id: computing-software.software-engineering.java.equals-hashcode-and-comparable-contracts
name: equals-hashcode-and-comparable-contracts
category: computing-software
field: software-engineering
product: java
tags: [java, equals-hashcode, comparable, comparator, object-contracts, hashmap-keys, jpa-entity-equality, consistent-with-equals]
level: practitioner
status: docs-checked
description: "Implement equals, hashCode, compareTo and Comparators that obey their contracts, including JPA entity equality and mutable-key traps."
sources: ["https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/Object.html#equals(java.lang.Object)", "https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/Comparable.html", "https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/Comparator.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# equals, hashCode and Comparable contracts

**Goal:** objects that behave in HashMaps, HashSets, TreeMaps and sorting; contract
violations here produce "the item is in the set but contains() says false".

## equals/hashCode
Contract: reflexive, symmetric, transitive, consistent, `x.equals(null)` false; and
equal objects MUST have equal hash codes.
```java
@Override public boolean equals(Object o) {
    return o instanceof Sku other && code.equals(other.code) && region == other.region;
}
@Override public int hashCode() { return Objects.hash(code, region); }
```
- Override both or neither; let the IDE generate them rather than hand-writing.
- `instanceof` vs `getClass()`: `instanceof` breaks symmetry if subclasses add state;
  make value classes `final`, or use `getClass() != o.getClass()`.
- Never let fields used in hashCode change while the object is in a hash collection;
  the entry becomes unreachable.
- Arrays: use `Arrays.equals/hashCode`; BigDecimal: `equals` is scale-sensitive
  (`2.0` != `2.00`), use `compareTo == 0` or normalise.

## JPA entities
Generated ids are null before persist, so id-based equality changes on save. Prefer a
natural/business key for equality, and keep lazy associations out of `equals`/`hashCode`.

## Comparable and Comparator
```java
static final Comparator<Emp> ORDER =
    Comparator.comparing(Emp::dept)
              .thenComparing(Emp::lastName, String.CASE_INSENSITIVE_ORDER)
              .thenComparingLong(Emp::id);
Comparator.nullsLast(Comparator.naturalOrder());
```
- Never `return a.x - b.x;`: integer overflow flips signs. Use `Integer.compare`.
- `compareTo` should be consistent with equals; otherwise TreeSet (uses compareTo) and
  HashSet (uses equals) disagree about duplicates (BigDecimal is the famous example).
- Ensure a total order (tie-breaker on a unique field) for stable pagination.

## Verify
- [ ] Tests for the equals/hashCode contracts pass (reflexive, symmetric, transitive, consistent).
- [ ] Sorting tests include ties, nulls and extreme values.

## Checked

- Date: 2026-10-28
- Confirmed in the Java SE 21 Javadoc (Object.equals/hashCode, Comparable, Comparator, Integer.compare, Arrays.equals pages): equals contract, equal objects need equal hash codes, hashCode consistency, compareTo consistent with equals (BigDecimal exception), nullsLast.
- Removed: Lombok and records claims, JPA constant-hashCode advice, EqualsVerifier.
Method: documentation only; no commands were run.
