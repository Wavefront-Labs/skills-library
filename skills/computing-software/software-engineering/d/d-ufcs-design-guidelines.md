---
id: computing-software.software-engineering.d.d-ufcs-design-guidelines
name: d-ufcs-design-guidelines
category: computing-software
field: software-engineering
product: d
tags: [d-ufcs-design-guidelines, ufcs, api-design, argument-order, ufcs-design, name-clash, selective-import, d]
level: practitioner
status: draft
description: "Put the primary subject first, keep templates range-friendly, avoid name clashes, and use selective imports so UFCS code stays readable and does not break."
sources:
  - https://dlang.org/spec/spec.html
  - https://dlang.org/phobos/index.html
  - https://dub.pm/
  - https://ddili.org/ders/d.en/index.html
  - https://dlang.org/articles.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Designing APIs for UFCS: argument order, ranges and overloads

Goal: write libraries that read well when chained.

- Subject first: `bool contains(R, E)(R haystack, E needle)` so `haystack.contains(needle)` works; for pipeline stages, take the range as the first parameter and return a range.
- Return types: `auto` for lazy results; callers pipe the result into the next stage.
- Avoid generic names (`find`, `map`) in your module if user code imports std.algorithm too; ambiguous symbol errors appear when two modules export the same name; resolve with `alias` or fully qualified call.
- Prefer free functions over methods for extension in generic code: they work on built-ins and third-party types without editing them.
- Use `@safe pure nothrow @nogc` and templates to let attributes infer.
- Properties: `@property` zero-arg free functions behave as fields (`str.lengthInChars`), but ordering of parentheses matters when the result is callable.

Gotchas:
- Order-of-arguments traps: `std.algorithm.startsWith(haystack, needle)`, `std.string.indexOf(haystack, needle)`, but `std.array.insertInPlace(array, pos, ...)`.
- Ambiguity errors with overloads imported from different modules.

Verify: write a short chain using your function after `map` and `filter`; it compiles without qualification.
