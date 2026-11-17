---
id: computing-software.software-engineering.java.nested-inner-local-and-anonymous-classes
name: nested-inner-local-and-anonymous-classes
category: computing-software
field: software-engineering
product: java
tags: [java, java-oop, inner-classes, static-nested-class, anonymous-classes, local-classes, outer-reference-leak]
level: practitioner
status: docs-checked
description: "Choose between static nested, inner, local and anonymous classes, avoid the hidden outer-instance reference leak, and know when a record is better."
sources: ["https://docs.oracle.com/javase/specs/jls/se21/html/jls-8.html#jls-8.1.3"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Nested, inner, local and anonymous classes

**Goal:** pick the narrowest class form and avoid accidental memory retention.

## Decision table
| Form | Has outer instance | Use for |
|---|---|---|
| `static class Node` (static nested) | no | helper types, builders, entries; default choice |
| `class Iter` (inner: a member class that is not static) | yes | iterators or views that need the outer state |
| local class inside a method | captures effectively-final locals | one-off helper with several methods |
| anonymous class | captures locals, implicit supertype | one-off implementation of an interface with several methods or state |
| record (nested records are implicitly static) | no | immutable data carriers |

## The leak
An inner class instance has an immediately enclosing instance. Handing such an object to a long-lived registry (listener, cache, executor, `ThreadLocal`) can pin the whole outer object and its graph, even if the inner class never uses it.
```java
class Screen {
    void init(EventBus bus) {
        bus.register(new Listener() { ... });   // anonymous class declared in an instance method keeps Screen reachable
    }
}
```
Fix: make the class `static` and pass only the data it needs.

## Gotchas
- Any local variable, parameter or exception parameter used but not declared in an inner class must be final or effectively final, and definitely assigned before the class body (JLS 8.1.3).
- Mutate a one-element array or an `AtomicInteger` only when the code cannot be restructured.

## Verify
Mark nested classes `static` unless they need the outer instance; review every non-static inner class and justify its outer reference.

## Checked

Method: docs-checked 2026-11-09 against JLS SE 21 chapter 8 (section 8.1.3 inner classes, effectively final capture, nested record). Dropped unconfirmed claims (lambda capture, serialization, javac naming, heap-dump and SpotBugs checks, qualified creation) and the unreadable dev.java source.
