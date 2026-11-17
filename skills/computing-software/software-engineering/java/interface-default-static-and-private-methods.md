---
id: computing-software.software-engineering.java.interface-default-static-and-private-methods
name: interface-default-static-and-private-methods
category: computing-software
field: software-engineering
product: java
tags: [java, default-methods, interface-evolution, static-interface-methods, diamond-problem, modern-java]
level: practitioner
status: docs-checked
description: "Design Java interfaces with default, static and private methods: evolving APIs without breaking implementers, diamond conflict rules, and when an abstract class fits better."
sources: ["https://dev.java/learn/interfaces/", "https://docs.oracle.com/javase/specs/jls/se21/html/jls-9.html#jls-9.4", "https://docs.oracle.com/javase/tutorial/java/IandI/defaultmethods.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Interface default, static and private methods

**Goal:** add capabilities to published interfaces safely and keep helper logic close
to the contract.

## Default methods: evolve without breaking implementers
```java
public interface Repository<T, ID> {
    Optional<T> findById(ID id);
    List<T> findAll();

    default List<T> findAllById(Collection<ID> ids) {     // added in v2: old impls still compile
        return ids.stream().map(this::findById).flatMap(Optional::stream).toList();
    }
}
```
Implementations can override with an efficient version (one SQL `IN` query). A class implementing the interface
gets the default without modification.

Limits: interfaces have no instance variables, so defaults cannot hold state; and an interface cannot declare a
method override-equivalent to a public method of `Object` (`equals`, `hashCode`, `toString`) that is not abstract
(JLS chapter 9: compile-time error).

## Static methods: factories and helpers
```java
public interface Money {
    static Money of(long cents, Currency c) { return new SimpleMoney(cents, c); }
    long cents();
}
Comparator.naturalOrder(); List.of(...);          // JDK examples
```
Interface static methods are implicitly public; call them via the interface name.

## Private methods
Share code between default methods without exposing it:
```java
default String describe() { return format(name()); }
default String describeShort() { return format(name().substring(0, 3)); }
private String format(String s) { return "[" + s + "]"; }
```

## Interface vs abstract class
| Need | Choose |
|---|---|
| multiple inheritance of type, API evolution | interface (+ defaults) |
| shared mutable state, constructors, protected members | abstract class |
| closed set of implementations | `sealed interface ... permits ...` |
A `sealed` interface limits its direct subclasses and subinterfaces to those known when it is declared (JLS 9.1.1.4).

## Gotchas
- Defaults calling other abstract methods must document that dependency (self-use).

## Checked
2026-11-01. Confirmed against JLS SE 21 chapter 9 (no instance variables, sealed interfaces, Object-method rule) and
the Oracle Java Tutorial page Default Methods (defaults on existing interfaces, implicit public static methods).
Removed: Java 8 library examples, Java 9 private-method version note, diamond conflict rules, Effective Java
reference, new-default clash gotcha (not on these pages).
Method: documentation only; no commands were run.

## Verify
- [ ] New interface methods in a published API come with a default or a major version bump.
- [ ] Default implementations are correct for every existing implementer (contract tests).
