---
id: computing-software.software-engineering.groovy.loops-iteration
name: loops-iteration
category: computing-software
field: software-engineering
product: groovy
tags: [groovy, loops-iteration]
level: intro
status: docs-checked
description: "Groovy loops: classic for, for-in over ranges, lists, arrays and maps, and the GDK times, upto, downto and step methods."
sources:
  - https://groovy-lang.org/semantics.html
  - https://github.com/apache/groovy/blob/master/src/main/java/org/codehaus/groovy/runtime/DefaultGroovyMethods.java
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Loops and iteration idioms
- Classic Java-style for loop: `for (int i = 0; i < 5; i += 1) { ... }`. The comma-separated form (`for (int fact = 1, i = 1; i <= count; i++, fact *= i)`) and multi-assignment in the loop header are also supported.
- `for (i in 0..9)` iterates a range; the same `for ... in` form works with any list, array, or Map, and also with the values of `map.values()`. Iterating a Map yields entries (`e.value`).
- The GDK adds numeric iteration methods on `Number` (in `DefaultGroovyMethods`): `times`, `upto`, `downto` and `step(to, stepNumber, closure)`.
- Collections also offer closure-based iteration such as `each` and `eachWithIndex`.

## Checked

2026-11-03. Confirmed against the Semantics chapter (looping structures: classic for, enhanced classic for, multi-assignment in for, for in loop) and the `DefaultGroovyMethods` source (`times`, `upto`, `downto`, `step`, `eachWithIndex`). Removed: claims about `break`, `continue` and `return` inside `each` closures, the ConcurrentModificationException note, and the self-check.

Method: documentation only; no commands were run.
