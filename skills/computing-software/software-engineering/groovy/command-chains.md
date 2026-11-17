---
id: computing-software.software-engineering.groovy.command-chains
name: command-chains
category: computing-software
field: software-engineering
product: groovy
tags: [groovy, command-chains, groovy-dsl]
level: advanced
status: docs-checked
description: "Groovy command chains (omitting dots and parens) for fluent English-like DSLs, and what parses to what."
sources:
  - https://groovy-lang.org/dsls.html
  - https://github.com/apache/groovy/blob/master/src/spec/doc/core-domain-specific-languages.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Command chains and optional syntax
- A chain `a b c d` equals `a(b).c(d)`; it works with multiple, closure and named arguments and can appear on the right of an assignment.
- Methods without arguments in the chain need parentheses; with an odd number of elements the chain ends in a property access.

## Gotchas

## Self-check
Build a two-word chain `show me x` handled by a script delegate with `show(...)` and `me(...)`.

## Checked

2026-11-02. Confirmed against the DSL chapter (command chains). Removed: the chloroquinine parse, closure-argument example, metaClass/extension and newline/groovysh claims.

Method: documentation only; no commands were run.
