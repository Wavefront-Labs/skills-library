---
id: computing-software.software-engineering.groovy.map-literals
name: map-literals
category: computing-software
field: software-engineering
product: groovy
tags: [groovy, map-literals, groovy-maps]
level: intro
status: docs-checked
description: "Groovy map literals, key quoting rules, property and bracket access, and default values."
sources:
  - https://groovy-lang.org/syntax.html
  - https://github.com/apache/groovy/blob/master/src/spec/doc/core-syntax.adoc
  - https://github.com/apache/groovy/blob/master/src/spec/doc/_working-with-collections.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Map literals and access
- `def m = [a: 1, 'b c': 2, (k): 3]`: bare keys are strings; wrap a variable in parens to use its value.
- Access: `m.a`, `m['a']`; a missing key reads as `null`.
- `[:]` is the empty map. Default type is `LinkedHashMap` (insertion order).
- `m.withDefault { [] }` wraps the map so reading a missing key returns and stores a value computed by the closure.

## Gotchas
- `[k: 1]` uses the string "k", not the variable `k`.
- `m.class` returns the key "class" (see identifiers-keywords).

## Self-check
`def k='x'; assert [(k):1].x == 1 && [k:1].k == 1`.

## Checked

2026-11-02. Confirmed against the Syntax chapter (maps) and Working with collections (withDefault, property access versus subscript). Removed: get(key, default) and getOrDefault claims.

Method: documentation only; no commands were run.
