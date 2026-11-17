---
id: computing-software.software-engineering.groovy.pitfalls-gotchas
name: pitfalls-gotchas
category: computing-software
field: software-engineering
product: groovy
tags: [groovy, pitfalls-gotchas]
level: practitioner
status: draft
description: "Frequent traps: GString keys, integer division, closures on null, == and equals, optional parentheses, property vs method, and map literal keys."
sources:
  - https://groovy-lang.org/style-guide.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Common Groovy pitfalls
- GString as map key; use `.toString()`.
- `def x = [:]` then `x.class` returns null; use `x.getClass()`.
- `(1..3).each { }` ranges are inclusive; `1..<3` exclusive.
- `'a' + 1` is `a1` but `1 + 'a'` fails with MissingMethod; use `"${1}a"`.
- `list.sort()` mutates; `list.sort(false)` copies.
- `String.split` uses regex; `tokenize` splits on chars.
- `return` in `each` just continues.
- Methods named like properties: `obj.name` calls `getName()` if present.
- Arrays are not lists: `[1,2] as int[]`.

## Gotchas
- Dynamic typos surface only at runtime; add tests or `@TypeChecked`.

## Self-check
Write a test for three of the traps above.
