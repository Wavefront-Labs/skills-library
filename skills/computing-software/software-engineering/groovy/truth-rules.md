---
id: computing-software.software-engineering.groovy.truth-rules
name: truth-rules
category: computing-software
field: software-engineering
product: groovy
tags: [groovy, truth-rules, groovy-truth]
level: practitioner
status: docs-checked
description: "What coerces to false in Groovy (null, empty, zero, false, empty matcher) and where truthiness applies."
sources:
  - https://groovy-lang.org/semantics.html
  - https://github.com/apache/groovy/blob/master/src/spec/doc/core-semantics.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Groovy truth rules
- False: `null`, `false`, `0`, empty `String`/`GString`, empty collection/map/array, empty iterator/enumeration, a `Matcher` with no match.
- True otherwise: non-empty collections, maps, strings and arrays, non-zero numbers, non-null object references and iterators with further elements.
- `if (list)` is the idiom for non-empty; `if (str)` for non-null and non-empty.

## Gotchas
- `'0'` and `'false'` are non-empty strings, so they are true.
- Implement `asBoolean()` to customise the truth of your own class.

## Self-check
`assert !'' && !null && !0 && 'false'`.

## Checked

2026-11-02. Confirmed against the Semantics chapter (The Groovy Truth: booleans, collections, matchers, iterators, maps, strings, numbers, object references, asBoolean). Removed: the list of statements the rules apply in, and the 0.0 and `x == true` gotchas.

Method: documentation only; no commands were run.
