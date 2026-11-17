---
id: computing-software.software-engineering.dart.dart-switch-patterns
name: dart-switch-patterns
category: computing-software
field: software-engineering
product: dart
tags: [dart, dart-records-patterns, switch-patterns]
level: practitioner
status: docs-checked
description: "Use switch expressions, object/list/map patterns, guards and sealed exhaustiveness."
sources: ["https://dart.dev/language/branches", "https://dart.dev/language/patterns", "https://dart.dev/language/pattern-types"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Switch expressions, patterns and guards
- `final s = switch (n) { 0 => 'zero', > 0 => 'pos', _ => 'neg' };` expression form without break or case colon.
- Patterns: `case [int a, int b]`, `case {'k': var v}`, `case Point(x: var x)`, `case int n when n > 3`, `if (obj case String s) ...`.
- Switch case bodies do not need `break`; an empty case falls through to the next case.
- Exhaustive over `sealed` types and enums; missing cases are compile errors.
Verify: add a new subtype of a sealed class and read analyzer warnings.

## Checked

Date: 2026-11-02. Confirmed on the Branches page: switch expressions, `when` guards, `if-case`, no `break` needed, empty cases fall through, exhaustiveness checking with `sealed` and enums; pattern forms on the Patterns and Pattern types pages.

Method: documentation only; no commands were run.
