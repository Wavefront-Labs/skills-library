---
id: computing-software.software-engineering.dart.dart-result-typed-errors
name: dart-result-typed-errors
category: computing-software
field: software-engineering
product: dart
tags: [dart, dart-design-patterns, result-typed-errors]
level: advanced
status: docs-checked
description: "Model success and failure with sealed classes and exhaustive switch instead of exceptions where failures are expected."
sources: ["https://dart.dev/language/class-modifiers", "https://dart.dev/language/patterns", "https://dart.dev/language/pattern-types"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Result types, sealed classes and error modelling
- `sealed class Result<T> {}` with `final class Ok<T> extends Result<T> { final T value; ... }` and `final class Err<T> ...`. The `sealed` modifier gives a known, enumerable set of direct subtypes (they can only exist in the same library) and makes the class implicitly abstract; the subtypes are not implicitly abstract.
- `switch (r) { case Ok(:final value): ...; case Err(:final error): ... }` uses object patterns that destructure through getters, and the compiler reports a switch that does not handle every subtype.
- If you do not want exhaustive switching, or want to add subtypes later without breaking the API, use `final` instead of `sealed`.
- Design guidance (judgement, not from the docs): use exceptions for exceptional cases and Results for validation and expected failures at boundaries; keep one style per layer and map exceptions to results at the repository boundary.

Verify: remove one case and read the analyzer's exhaustiveness error.

## Checked

Checked 2026-11-08 against https://dart.dev/language/class-modifiers (sealed section), https://dart.dev/language/patterns and https://dart.dev/language/pattern-types (object patterns); the pages were read for the cited sections, not end to end.

Method: documentation only; no commands were run.
