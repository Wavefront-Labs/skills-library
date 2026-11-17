---
id: computing-software.software-engineering.groovy.switch-case
name: switch-case
category: computing-software
field: software-engineering
product: groovy
tags: [groovy, switch-case, groovy-control]
level: practitioner
status: docs-checked
description: "Groovy switch matches via isCase: ranges, classes, regex, lists, closures; fall-through and default."
sources:
  - https://groovy-lang.org/semantics.html
  - https://github.com/apache/groovy/blob/master/src/spec/doc/core-semantics.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# switch with isCase classification
```groovy
def kind(x) {
  switch (x) {
    case 0..9:        return 'digit'
    case ~/[a-z]+/:   return 'word'
    case Integer:     return 'int'
    case [true, null]:return 'special'
    case { it instanceof Map }: return 'map'
    default:          return 'other'
  }
}
```
- Each `case` calls `caseValue.isCase(switchValue)`; implement `isCase` on your own classes.
- Fall-through occurs without `break`/`return`, as in Java. Switch expressions (JEP 361) with `->` arms are also supported: arrow arms do not fall through, and an unmatched selector throws `IllegalStateException`.

## Gotchas
- Order matters: `case Integer` before `case 0..9` hides the range.
- A closure case value receives the switch value as `it`.

## Self-check
`assert kind(5) == 'digit' && kind('ab') == 'word'`.

## Checked

2026-11-02. Confirmed against the Semantics chapter (switch / case comparison kinds, closure case values, switch expressions). Removed: the Groovy 4 version claim and the String/GString matching gotcha.

Method: documentation only; no commands were run.
