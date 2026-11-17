---
id: computing-software.software-engineering.java.unnamed-variables-and-patterns
name: unnamed-variables-and-patterns
category: computing-software
field: software-engineering
product: java
tags: [java, java-22, jep-456, unnamed-variables, pattern-matching, underscore]
level: practitioner
status: docs-checked
description: "Use the underscore for unused variables and pattern components (final in Java 22, JEP 456); know where it is legal and what it does not do."
sources: ["https://openjdk.org/jeps/456"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Unnamed variables and patterns (`_`)

**Version note:** a preview feature in Java 21 (JEP 443, needs `--enable-preview`); final in Java 22 (JEP 456). The underscore was a valid identifier in Java 1.0; compile-time warnings for it began in Java 8 and became errors in Java 9 (JEP 213). Identifiers of two or more characters such as `_age`, and underscores as digit separators (`123_456_789`), are unchanged.

## Where `_` is allowed
```java
try { parse(s); } catch (NumberFormatException _) { return 0; }      // unused exception parameter
for (var _ : list) count++;                                          // unused loop variable
try (var _ = ScopedContext.acquire()) { ... }                         // unused resource (example from the JEP)
int _ = compute();                                                    // result you must call but ignore

if (shape instanceof Circle(var r)) ...
switch (box) {
    case Box(RedBall _), Box(BlueBall _) -> processBox(box);          // several patterns in one case, all unnamed
    case Box(GreenBall _)                -> stopProcessing();
    case Box(_)                          -> pickAnotherBox();         // unnamed pattern: matches any component
}
```
An unnamed pattern variable can carry a type (`RedBall _`) or use `var _`. A bare `_` as a pattern (no type) matches anything of the component type and appears nested inside a record pattern, as in `Box(_)`. An unnamed variable also works as a lambda parameter, for example `_ -> "NODATA"`.

## Rules
- You cannot read `_`; it is not a name.
- It is for local variables, exception parameters, resources, lambda parameters and pattern variables. Not for fields or method parameters.
- A case label with several patterns is allowed only when none of them declares a named pattern variable.

## Gotchas
- Does not suppress side effects: `int _ = compute();` still calls `compute()`.
- On Java 21, the same code needs `--enable-preview`; tools and linters built for Java 21 or earlier may reject it. Keep IDE, build and CI on one language level.

## Verify
Compile a file using `catch (NumberFormatException _)` on a JDK 22 or newer toolchain; confirm the same file fails on an older language level.

## Checked
2026-11-03. Confirmed against JEP 456: preview in 21 via JEP 443, final in 22, history of the underscore identifier (warning in 8, error in 9), unchanged identifiers and digit separators, the allowed positions (local declarations, catch parameters, try-with-resources, lambda parameters, pattern variables), multi-pattern case labels and the bare `_` pattern.
Removed (not in the page read): the `javac --release` flag lines and example calls such as `map.forEach` and `queue.poll`.
Method: documentation only; no commands were run.
