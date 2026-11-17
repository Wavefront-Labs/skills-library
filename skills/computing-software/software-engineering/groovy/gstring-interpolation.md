---
id: computing-software.software-engineering.groovy.gstring-interpolation
name: gstring-interpolation
category: computing-software
field: software-engineering
product: groovy
tags: [groovy, gstring-interpolation]
level: practitioner
status: docs-checked
description: "GString interpolation with dollar-brace and dollar-dot, closures for lazy evaluation, and the String/GString equality trap."
sources:
  - https://groovy-lang.org/syntax.html
  - https://github.com/apache/groovy/blob/master/src/spec/doc/core-syntax.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GString interpolation and lazy evaluation
- `"$name"`, `"${obj.prop}"`, `"$obj.prop.sub"` (dotted path only, no method calls without braces).
- Eager: `"${x}"` captures the value when the GString is created. Lazy: `"${-> x}"` re-evaluates on each `toString()`.
```groovy
def x = 1; def eager = "v=${x}"; def lazy = "v=${-> x}"
x = 2
assert eager == 'v=1' && lazy == 'v=2'
```

## Gotchas
- `"$a.b()"` parses as `${a.b}()`; use `"${a.b()}"`.
- GString hashCode differs from String's: never use as HashMap key or in a Set without `.toString()`.
- Passing a GString to a Java API taking `String` coerces automatically, but it can leak into `List<String>` generics.

## Self-check
Run the snippet; the assert should hold.

## Checked

2026-11-02. Confirmed against the Syntax chapter (string interpolation, closure expressions and lazy evaluation, Java interoperability, GStrings in collections, GString and String hashCodes). Removed: nothing (the unread gapi/groovy-jdk links were replaced by the pages read).

Method: documentation only; no commands were run.
