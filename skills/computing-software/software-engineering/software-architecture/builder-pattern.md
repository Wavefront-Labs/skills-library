---
id: computing-software.software-engineering.software-architecture.builder-pattern
name: builder-pattern
category: computing-software
field: software-engineering
product: software-architecture
tags: [software-architecture, design-patterns, creational-patterns, builder-pattern, gof, fluent-api, telescoping-constructor, immutable-objects, test-data-builders]
level: practitioner
status: draft
description: "Use the Builder pattern to construct complex or immutable objects step by step, replace telescoping constructors, validate at build(), and build test data."
sources: ["Design Patterns: Elements of Reusable Object-Oriented Software (Gamma, Helm, Johnson, Vlissides), Builder", "Effective Java, 3rd ed. (Bloch), Item 2", "https://refactoring.guru/design-patterns/builder"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Builder

**Intent (GoF):** separate the construction of a complex object from its representation,
so the same construction process can create different representations. In everyday code
(Bloch's variant): build an object with many optional parameters readably.

## When it fits
- Constructors with many parameters, several optional (telescoping constructors,
  boolean flags nobody can read at the call site).
- Immutable objects that need step-by-step assembly.
- Test data with sensible defaults where each test overrides a few fields.

## Bloch-style builder
```java
public final class HttpRequest {
    private final URI uri; private final Duration timeout; private final Map<String,String> headers;
    private HttpRequest(Builder b) { uri = b.uri; timeout = b.timeout; headers = Map.copyOf(b.headers); }
    public static Builder newBuilder(URI uri) { return new Builder(uri); }   // required args up front
    public static final class Builder {
        private final URI uri; private Duration timeout = Duration.ofSeconds(30);
        private final Map<String,String> headers = new HashMap<>();
        private Builder(URI uri) { this.uri = Objects.requireNonNull(uri); }
        public Builder timeout(Duration t) { this.timeout = t; return this; }
        public Builder header(String k, String v) { headers.put(k, v); return this; }
        public HttpRequest build() {
            if (timeout.isNegative()) throw new IllegalStateException("timeout < 0");
            return new HttpRequest(this);
        }
    }
}
```
- Required parameters in the builder's constructor/factory; optional ones as methods.
- Validate invariants in `build()` (cross-field rules), so a half-configured object never exists.
- Lombok `@Builder`, Kotlin named/default args, C# object initialisers + `required`,
  Python keyword arguments, TS options objects make hand-written builders unnecessary
  in many languages.

## GoF form
A Director drives an abstract Builder (`buildHeader`, `buildBody`) and concrete builders
produce different representations (HTML vs PDF). Use when the same assembly steps must
produce different outputs.

## Test data builders
`anOrder().withStatus(PAID).withLines(2).build()` - defaults keep tests short and
resilient to new required fields.

## Pitfalls
- Builders for 2-3 field classes: noise.
- Mutable builders reused across threads or across `build()` calls leaking state.
- Forgetting to copy collections in `build()`.

## Verify
- [ ] Missing required fields are impossible (compile-time) or rejected in `build()`.
- [ ] Built objects are immutable.
