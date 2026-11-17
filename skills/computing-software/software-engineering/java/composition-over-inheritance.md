---
id: computing-software.software-engineering.java.composition-over-inheritance
name: composition-over-inheritance
category: computing-software
field: software-engineering
product: java
tags: [java, java-oop, composition-over-inheritance, delegation, liskov-substitution, fragile-base-class, final-classes]
level: practitioner
status: draft
description: "Replace fragile subclassing with composition and delegation in Java; apply the Liskov rule, design for inheritance or forbid it, and use sealed types to close hierarchies."
sources: ["https://dev.java/learn/inheritance/", "https://docs.oracle.com/javase/specs/jls/se21/html/jls-8.html#jls-8.4.8"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Composition over inheritance

**Goal:** reuse behaviour without coupling a subclass to its parent's implementation details.

## The fragile base class
```java
class CountingSet<E> extends HashSet<E> {
    int added;
    @Override public boolean add(E e) { added++; return super.add(e); }
    @Override public boolean addAll(Collection<? extends E> c) { added += c.size(); return super.addAll(c); }
}   // addAll calls add internally: every element is counted twice
```
Subclasses depend on *self-use* of overridable methods, which is undocumented and can change in a library upgrade.

## Compose and delegate
```java
final class CountingSet<E> implements Set<E> {
    private final Set<E> delegate;
    private int added;
    CountingSet(Set<E> delegate) { this.delegate = delegate; }
    public boolean add(E e) { added++; return delegate.add(e); }
    public boolean addAll(Collection<? extends E> c) { added += c.size(); return delegate.addAll(c); }
    // forward the rest (or extend a ForwardingSet from Guava)
}
```

## Rules
1. Inherit only for a true is-a relationship where every subclass honours the parent's contract (Liskov): no strengthened preconditions, no weakened postconditions, no new checked exceptions.
2. Classes not designed for extension should be `final`; if extensible, document which methods are self-used (the `@implSpec` Javadoc tag) and never call overridable methods from constructors.
3. Prefer `sealed` hierarchies (Java 17+) when the set of subtypes is closed.
4. Share behaviour through interfaces with default methods or small collaborator objects.

## Gotchas
- Constructor calling an overridden method sees uninitialised subclass fields.
- Inheriting from `Thread`, `ArrayList`, `HashMap` or `Exception` just to add a field is almost always the wrong move (exceptions are the usual legitimate exception).

## Verify
Check that every `extends` of a concrete class in your code can answer "would a delegate field work?"; unit tests for each subclass should run the parent's test suite (contract test) unchanged.
