---
id: computing-software.software-engineering.java.sealed-types-and-pattern-matching
name: sealed-types-and-pattern-matching
category: computing-software
field: software-engineering
product: java
tags: [java, sealed-classes, pattern-matching-switch, record-patterns, algebraic-data-types, exhaustive-switch, modern-java, java-21, java-data-modeling]
level: practitioner
status: docs-checked
description: "Model closed hierarchies with sealed interfaces and records, and process them with exhaustive pattern-matching switch, record patterns and guards (Java 21)."
sources: ["https://openjdk.org/jeps/409", "https://openjdk.org/jeps/441", "https://openjdk.org/jeps/440", "https://openjdk.org/jeps/456"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Sealed types and pattern matching for switch

**Goal:** represent "one of these known variants" (results, events, AST nodes) so the
compiler forces every switch to handle every case.

## Sealed hierarchy of records
```java
public sealed interface PaymentResult
        permits Approved, Declined, NeedsAction {}
public record Approved(String txId) implements PaymentResult {}
public record Declined(String reason, boolean retryable) implements PaymentResult {}
public record NeedsAction(URI redirect) implements PaymentResult {}
```
- Permitted subclasses must be in the same module (or same package if unnamed module).
  If in the same file, `permits` can be omitted.
- Each subclass must be `final` (records are), `sealed`, or `non-sealed`.

## Exhaustive switch (Java 21)
```java
String message = switch (result) {
    case Approved(var txId)                       -> "OK " + txId;
    case Declined(var reason, var retry) when retry -> "Retry later: " + reason;
    case Declined(var reason, var retry)            -> "Declined: " + reason;
    case NeedsAction(var uri)                      -> "Go to " + uri;
};   // no default needed; compile error if a variant is missing
```
- Do NOT add `default` to sealed switches: it silences the compile error you want when
  a new variant is added.
- Order matters: a guarded case must precede an unguarded case for the same type
  (dominance is a compile error otherwise).
- `case null ->` handles null explicitly; without it a null selector throws NPE.
- Unnamed patterns (`_`, JEP 456, final in Java 22) mark ignored components: `case Declined(var r, _)`.

## instanceof patterns
`if (obj instanceof String s && !s.isBlank()) { use(s); }` - no cast needed.

## Where this beats the Visitor pattern
Adding an operation is a new switch, no `accept/visit` boilerplate; adding a variant
breaks compilation in every switch that must handle it. Visitor still fits when variants
come from outside your module (sealed requires you own them all).

## Gotchas
- Separately compiled code: if a library adds a variant, old compiled switches throw
  `MatchException` at runtime. Recompile consumers.

## Checked
2026-10-28: Confirmed in JEP 409 and JLS 8: permitted subclasses in the same module, permits omitted when all are in the same compilation unit, final/sealed/non-sealed; JEP 441 and JLS 15: MatchException when no label applies; JEP 456 for unnamed patterns. Removed the dev.java source (page 404) and the preview-flag bullet.
Method: documentation only; no commands were run.

## Verify
- [ ] Add a dummy variant: every relevant switch fails to compile.
- [ ] No `default` branch in switches over sealed types.
