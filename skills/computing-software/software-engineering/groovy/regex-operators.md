---
id: computing-software.software-engineering.groovy.regex-operators
name: regex-operators
category: computing-software
field: software-engineering
product: groovy
tags: [groovy, regex-operators, groovy-regex]
level: practitioner
status: docs-checked
description: "Groovy regex operators =~ (find), ==~ (exact match), ~ (Pattern), and Matcher indexing."
sources:
  - https://groovy-lang.org/operators.html
  - https://github.com/apache/groovy/blob/master/src/spec/doc/core-operators.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Find, match and pattern operators
- `~/re/` makes a `java.util.regex.Pattern`.
- `s =~ /re/` returns a `Matcher` (find); truthy if a match exists. `s ==~ /re/` is a boolean full-match.
- A `Matcher` coerces to boolean by calling `find()`; to loop over matches call `find()` on the matcher or use the `iterator` DGM.

## Gotchas
- `=~` in an `if` calls `find()` on the matcher it creates.
- `==~` anchors the full string; `=~` does not.

## Self-check
`assert 'ab12' ==~ /[a-z]+\d+/ && ('x9' =~ /\d/)`.

## Checked

2026-11-02. Confirmed against the Operators chapter (pattern, find, match operators and comparing find vs match). Removed: the group-indexing example, reset() and thread-safety claims.

Method: documentation only; no commands were run.
