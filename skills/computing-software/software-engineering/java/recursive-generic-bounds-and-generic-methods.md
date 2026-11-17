---
id: computing-software.software-engineering.java.recursive-generic-bounds-and-generic-methods
name: recursive-generic-bounds-and-generic-methods
category: computing-software
field: software-engineering
product: java
tags: [java, java-generics, recursive-generic-bounds, generic-methods, self-types, comparable-bound, fluent-builders, bounded-types]
level: advanced
status: draft
description: "Write generic methods and self-referential bounds like <T extends Comparable<? super T>> and Builder<T extends Builder<T>> for fluent inheritance-safe APIs."
sources: ["https://dev.java/learn/generics/", "https://docs.oracle.com/javase/specs/jls/se21/html/jls-4.html#jls-4.5", "https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/Collections.html#max(java.util.Collection)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Generic methods and recursive bounds

## Generic methods
Type parameters before the return type; inferred from arguments:
```java
static <T> List<T> repeat(T item, int n) { return Collections.nCopies(n, item); }
List<String> xs = repeat("a", 3);         // no explicit <String>
Util.<String>emptyList();                  // explicit witness when inference lacks a target
```

## Comparable bounds
The JDK signature is `<T extends Object & Comparable<? super T>> T max(Collection<? extends T>)`:
```java
static <T extends Comparable<? super T>> T maxOf(List<? extends T> xs) { ... }
```
`? super T` lets `java.sql.Timestamp extends Date` work when `Comparable<Date>` is declared on the parent. `T extends Comparable<T>` rejects such subclasses.

## Self-referential (CRTP) bound for fluent inheritance
```java
abstract class Builder<T extends Builder<T>> {
    String name;
    abstract T self();
    T name(String n) { this.name = n; return self(); }
}
final class CarBuilder extends Builder<CarBuilder> {
    int wheels;
    CarBuilder self() { return this; }
    CarBuilder wheels(int w) { wheels = w; return this; }
}
new CarBuilder().name("x").wheels(4);     // name() returns CarBuilder, so chaining continues
```
The same trick backs `Enum<E extends Enum<E>>`.

## Intersection bounds
`<T extends Number & Comparable<T>>`: class first, then interfaces. Method calls are limited to the members of all bounds; erasure uses the first bound.

## Gotchas
- A self type is not enforced: `class Evil extends Builder<CarBuilder>` compiles. Use sealed hierarchies or reviews for strictness.
- Wildcard capture: a helper method `private <T> void swapHelper(List<T> l)` lets `swap(List<?> l)` modify the list.
- Static generic factory vs constructor: the diamond `new Box<>(x)` infers from arguments or target type, a constructor has no type-parameter list of its own beyond the class.

## Verify
Compile with `-Xlint:unchecked,rawtypes`; add a test sorting a `List<java.sql.Timestamp>` through your `maxOf` to prove the `? super T` bound.
