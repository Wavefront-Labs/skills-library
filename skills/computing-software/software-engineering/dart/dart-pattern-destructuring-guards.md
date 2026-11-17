---
id: computing-software.software-engineering.dart.dart-pattern-destructuring-guards
name: dart-pattern-destructuring-guards
category: computing-software
field: software-engineering
product: dart
tags: [dart, pattern-destructuring-guards]
level: advanced
status: docs-checked
description: "Use Dart 3 patterns in switch, if-case and declarations: list, map, object patterns, guards and wildcard."
sources: ["https://dart.dev/language/patterns", "https://dart.dev/language/pattern-types", "https://dart.dev/language/branches"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Patterns
- `var (a, b) = (1, 2);`, `case [int x, int y]`, `case {'k': var v}`, `case Point(x: var px)`, `case int n when n > 0`.
- `||` and `&&` patterns, relational `> 5`, cast `as`, null-check `?`, null-assert `!`, wildcard `_`.
- `if (json case {'id': int id})` narrows without a cast.
- Switch expressions: `final s = switch (x) { 0 => 'zero', _ => 'other' };`.
Verify: a switch over a sealed type with a missing case fails analysis.

## Checked

Date: 2026-11-02. Confirmed on the Patterns, Pattern types and Branches pages: logical-or and logical-and, relational, cast, null-check, null-assert and wildcard patterns, `when` guards, if-case, switch expressions. Removed the StateError claim (not stated).

Method: documentation only; no commands were run.
