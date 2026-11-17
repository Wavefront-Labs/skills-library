---
id: computing-software.software-engineering.java.builder-pattern-and-static-factories
name: builder-pattern-and-static-factories
category: computing-software
field: software-engineering
product: java
tags: [java, java-oop, builder-pattern, static-factory-methods, telescoping-constructors, immutable-objects, with-methods]
level: practitioner
status: draft
description: "Build immutable Java objects with many fields: static factories, a hand-written builder with validation in build(), and when records or Lombok builders suffice."
sources: ["https://dev.java/learn/classes-objects/", "https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/List.html#of(E...)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Builder pattern and static factory methods

**Goal:** readable construction of objects with many or optional fields, without telescoping constructors or mutable setters.

## Static factories first
Named factories explain intent, can cache, and can return subtypes: `Duration.ofSeconds(5)`, `List.of(...)`, `Money.of("USD", 10)`. Keep the constructor private.

## Builder when more than about four parameters or several optional ones
```java
public final class HttpRequestSpec {
    private final URI uri; private final String method; private final Duration timeout;
    private HttpRequestSpec(Builder b) {
        this.uri = Objects.requireNonNull(b.uri, "uri");
        this.method = b.method; this.timeout = b.timeout;
        if (timeout.isNegative()) throw new IllegalArgumentException("timeout");
    }
    public static Builder builder(URI uri) { return new Builder(uri); }
    public static final class Builder {
        private final URI uri; private String method = "GET"; private Duration timeout = Duration.ofSeconds(30);
        private Builder(URI uri) { this.uri = uri; }
        public Builder method(String m) { this.method = m; return this; }
        public Builder timeout(Duration t) { this.timeout = t; return this; }
        public HttpRequestSpec build() { return new HttpRequestSpec(this); }
    }
}
```
- Put required fields in the builder factory signature so incomplete objects cannot be built.
- Validate in the target constructor or `build()` (invariants across fields), not in setters.
- Copy mutable inputs defensively (`List.copyOf`).

## Alternatives
- Records for plain carriers (with a compact constructor for validation); add a `withX` method or a nested builder for >5 components.
- Lombok `@Builder` or Immutables generate the boilerplate; both are compile-time, so keep them in annotation-processor paths.

## Gotchas
- A builder is not thread-safe or reusable unless documented; `build()` twice should yield independent objects.
- Do not expose the builder's mutable collections.

## Verify
Unit test that `build()` with a missing required value fails with a clear message, and that mutating the input list after `build()` does not change the object.
