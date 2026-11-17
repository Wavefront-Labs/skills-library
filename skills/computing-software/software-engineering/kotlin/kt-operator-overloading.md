---
id: computing-software.software-engineering.kotlin.kt-operator-overloading
name: kt-operator-overloading
category: computing-software
field: software-engineering
product: kotlin
tags: [kotlin, kt-functions, operator-overloading]
level: practitioner
status: docs-checked
description: "Overload operators via conventions and write infix functions without surprising behaviour."
sources: ["https://kotlinlang.org/docs/operator-overloading.html", "https://kotlinlang.org/docs/functions.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Operator overloading and infix functions
- Mark `operator fun plus(other: V): V`, `get`, `set`, `invoke`, `compareTo`, `contains`; the language translates `a + b` to `a.plus(b)`, `a in b` to `b.contains(a)`, `a < b` to `a.compareTo(b) < 0`, `a(i)` to `a.invoke(i)`.
- `==` translates to `a?.equals(b) ?: (b === null)`; `===` is identity. `a += b` resolves to `plusAssign` or to `a = a + b`; if both fit, the compiler reports an ambiguity error.
- `infix` functions must be members or extensions with a single parameter: `infix fun Int.shl(x: Int): Int`.
- Only overload when the meaning is the mathematical one (vectors, money, matrices).
Verify: add `equals`/`hashCode`/`compareTo` consistency tests.

## Checked

Date: 2026-11-02. Confirmed on kotlinlang.org docs (operator-overloading.html, functions.html): translation table for plus, contains, compareTo, invoke, equals, plusAssign ambiguity; infix requirements. Removed as not stated there: iterator and componentN (not read), and the `2 pow 3` example.

Method: documentation only; no commands were run.
