---
id: computing-software.software-engineering.groovy.string-gdk-methods
name: string-gdk-methods
category: computing-software
field: software-engineering
product: groovy
tags: [groovy, string-gdk-methods, groovy-gdk-strings]
level: practitioner
status: docs-checked
description: "Everyday String GDK methods from StringGroovyMethods: tokenize, padLeft, center, take, drop, reverse, capitalize, isInteger, readLines, getAt, minus, multiply."
sources:
  - https://github.com/apache/groovy/blob/master/src/main/java/org/codehaus/groovy/runtime/StringGroovyMethods.java
  - https://groovy-lang.org/groovy-dev-kit.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# String GDK methods
These are defined in `StringGroovyMethods` (mostly on `CharSequence`):
- `padLeft(Number numberOfChars, CharSequence padding)` and `center(...)` pad a string to a width; `capitalize()`, `reverse()`, `take(int)`, `drop(int)` are available.
- `isInteger()` and `isNumber()` test whether the text parses as a number.
- `readLines()` returns the lines of the text as a `List<String>`; `eachLine` iterates them.
- `tokenize` is defined there as well.
- `getAt` with an int index or an `IntRange`/`Range` gives subscripts such as `s[0]` and `s[1..3]`; `getAt(CharSequence, Collection)` accepts several indices.
- Operators map to methods: `s * n` is `multiply(CharSequence, Number)`, `s - x` is `minus(CharSequence, Object)` and `+` is `plus`.

## Checked

2026-11-03. Confirmed against the `StringGroovyMethods` source (signatures listed above). Removed: code snippets with asserted values, negative-index behaviour, the description of how `minus` and `tokenize` differ from `split`, and `String.size()`.

Method: documentation only; no commands were run.
