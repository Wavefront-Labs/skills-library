---
id: computing-software.software-engineering.dart.dart-records
name: dart-records
category: computing-software
field: software-engineering
product: dart
tags: [dart, dart-records-patterns, records]
level: practitioner
status: docs-checked
description: "Return multiple values with records, destructure them and use named fields and structural equality."
sources: ["https://dart.dev/language/records", "https://dart.dev/language/patterns"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Records, destructuring and multiple returns
- `(int, String) r = (1, 'a');` positional fields `$1`, `$2`; named `({int a, int b}) p = (a: 1, b: 2);`.
- Structural equality: records with equal fields are `==`; they are immutable.
- Destructure: `var (x, y) = pair;` `final (:a, :b) = p;`.
- Records need a language version of at least 3.0.
Verify: `(1, 2) == (1, 2)` is true.

## Checked

Date: 2026-11-02. Confirmed on the Records page: positional fields `$1`, `$2`, named fields, immutability, equality by shape and field values, language version 3.0; destructuring on the Patterns page. Removed the advice to prefer classes (not stated).

Method: documentation only; no commands were run.
