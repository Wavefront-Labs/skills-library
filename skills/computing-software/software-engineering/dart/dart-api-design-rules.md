---
id: computing-software.software-engineering.dart.dart-api-design-rules
name: dart-api-design-rules
category: computing-software
field: software-engineering
product: dart
tags: [dart, dart-style, api-design-rules]
level: advanced
status: docs-checked
description: "Design public APIs following Effective Dart: names, parameters, equality and avoiding one-member classes."
sources: ["https://dart.dev/effective-dart/design"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Effective Dart design rules
- AVOID positional boolean parameters (use a named parameter; linter rule `avoid_positional_boolean_parameters`): `Task(true)` is unreadable at the call site.
- AVOID defining a one-member abstract class when a simple function will do, and AVOID classes that contain only static members; use functions or top-level declarations.
- PREFER making fields and top-level variables `final`; PREFER making declarations private.
- DO override `hashCode` if you override `==`; DO make `==` obey the mathematical rules of equality; AVOID custom equality for mutable classes; DON'T make the parameter to `==` nullable.
- AVOID using `dynamic` unless you want to disable static checking; DO annotate return and parameter types on function declarations.
- DO use `Future<void>` as the return type of asynchronous members that produce no value but that callers may need to await; use `void` only when no caller needs to await or handle failure.
- AVOID returning nullable `Future`, `Stream` and collection types; AVOID returning `this` just to enable a fluent interface.

Verify: review the public API of the package (for example the generated `dart doc` output) against these rules.

## Checked

Checked 2026-11-08 against https://dart.dev/effective-dart/design. The guideline headings and the sections on positional booleans and Future<void> were read; the rest of the long page was confirmed by guideline heading only. Removed: the unsourced phrase "avoid dynamic in public signatures" (replaced by the documented rule) and the "do not make fields public mutable state" wording (replaced by the documented final-fields rule).

Method: documentation only; no commands were run.
