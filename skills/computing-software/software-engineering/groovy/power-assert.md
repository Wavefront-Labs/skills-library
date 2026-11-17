---
id: computing-software.software-engineering.groovy.power-assert
name: power-assert
category: computing-software
field: software-engineering
product: groovy
tags: [groovy, power-assert, groovy-testing]
level: intro
status: docs-checked
description: "Groovy assert prints a value trace on failure; add custom messages and know what it evaluates."
sources:
  - https://groovy-lang.org/testing.html
  - https://github.com/apache/groovy/blob/master/src/spec/doc/core-testing-guide.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Power assert and assert messages
```groovy
def a = [1, 2]
assert a.size() == 3 : 'expected three elements'
```
- A failing assertion prints the evaluation results from the outer to the inner expression.
- `assert expression1 : expression2` uses `expression2` as the custom error message (Java syntax).
- Groovy enables assertions by default and cannot disable them (Java needs `-ea`).
- A failed assertion throws `java.lang.AssertionError` with an extended message.

## Gotchas
- Side-effecting methods in the asserted expression can make the printed message misleading, because the message builder stores references to instances, not copies.

## Checked

2026-11-02. Confirmed against the Testing guide (Power Assertions section). Removed: the `PowerAssertionError` name and the input-validation advice.

Method: documentation only; no commands were run.

## Self-check
Run the snippet and read the trace.
