---
id: computing-software.software-engineering.java.optional-usage-rules
name: optional-usage-rules
category: computing-software
field: software-engineering
product: java
tags: [java, java-optional, null-handling, nullpointerexception, orelsethrow, jspecify, nullable-annotations]
level: practitioner
status: docs-checked
description: "Use java.util.Optional as intended (return types for maybe-absent results), avoid its anti-patterns, and pair it with nullness annotations like JSpecify."
sources: ["https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/Optional.html", "https://dev.java/learn/api/streams/optionals/", "https://jspecify.dev/docs/user-guide/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Optional usage rules

**Goal:** make "may be absent" visible in method signatures without turning code into
`Optional` soup or creating new NPE sources.

## Intended use
`Optional<T>` is a RETURN type for queries that may legitimately find nothing:
```java
Optional<User> findByEmail(String email);

User u = repo.findByEmail(e).orElseThrow(() -> new NotFound("user " + e));
String name = repo.findByEmail(e).map(User::displayName).orElse("guest");
repo.findByEmail(e).ifPresentOrElse(this::notify, this::logMissing);
```

## Rules
1. Never return `null` from a method declared `Optional`; return `Optional.empty()`.
2. Do not use Optional for fields, method parameters, or collection elements. For
   collections, return an empty collection, never `Optional<List<T>>`.
3. Avoid `isPresent()` + `get()`; use `map`/`orElse`/`orElseThrow`. Plain `get()` is
   the same as an NPE with a different name (`orElseThrow()` without args is the
   explicit form).
4. `orElse(expensive())` evaluates the argument ALWAYS; use `orElseGet(() -> expensive())`
   for costly defaults or ones with side effects.
5. `Optional.of(x)` throws if x is null; use `ofNullable` at boundaries with legacy code.
6. Avoid `Optional` in DTOs and JPA entities.
7. Chaining fallbacks: `a().or(() -> b())` (Java 9+). Into streams: `opt.stream()`.

## Nullness annotations for everything else
For parameters and fields, annotate instead: JSpecify `@NullMarked` on the package and
`@Nullable` on the exceptions; check with NullAway or IntelliJ inspections. This covers
the cases Optional should not.

## Verify
- [ ] grep for `Optional<` in field and parameter declarations returns nothing.
- [ ] No `.get()` on Optional without a preceding guarantee; static analysis on in CI.

## Checked

- Date: 2026-10-28
- Confirmed in the Java SE 21 Optional Javadoc: intended use as a method return type, empty(), orElseGet, or/stream, of vs ofNullable; JSpecify user guide for @NullMarked/@Nullable.
- Removed: OptionalInt/OptionalDouble, Serializable and Jackson jdk8 module claims, Error Prone check name.
Method: documentation only; no commands were run.
