---
id: computing-software.software-engineering.groovy.safe-navigation-elvis
name: safe-navigation-elvis
category: computing-software
field: software-engineering
product: groovy
tags: [groovy, safe-navigation-elvis, groovy-operators]
level: practitioner
status: docs-checked
description: "Null-safe navigation ?., Elvis ?:, Elvis assignment ?=, and spaceship <=> in Groovy."
sources:
  - https://groovy-lang.org/operators.html
  - https://github.com/apache/groovy/blob/master/src/spec/doc/core-operators.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Safe navigation and Elvis operators
- Safe navigation `a?.b?.c` returns null instead of throwing NPE.
- Elvis `x ?: 'default'` uses Groovy truth (empty string and 0 also fall through).
- Elvis assignment `x ?= 'default'` and safe index `a?[0]` were introduced in Groovy 3.0.0.
- Spaceship `a <=> b` delegates to `compareTo`.
- Ternary `c ? a : b`.

## Gotchas
- `?:` triggers on any false-ish value (Groovy truth), not only null; for null-only use `x != null ? x : d`.

## Self-check
`assert null?.length() == null && ('' ?: 'd') == 'd'`.

## Checked

2026-11-02. Confirmed against the Operators chapter (safe navigation, Elvis, Elvis assignment, safe index, spaceship, ternary). Removed: the -1/0/1 claim, the call-chain gotcha and the version hedges.

Method: documentation only; no commands were run.
