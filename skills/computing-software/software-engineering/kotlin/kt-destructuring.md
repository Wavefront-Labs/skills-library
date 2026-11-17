---
id: computing-software.software-engineering.kotlin.kt-destructuring
name: kt-destructuring
category: computing-software
field: software-engineering
product: kotlin
tags: [kotlin, kt-classes, destructuring]
level: intro
status: docs-checked
description: "Unpack data classes, pairs, maps and lambda parameters with Kotlin destructuring declarations and componentN functions."
sources: ["https://kotlinlang.org/docs/destructuring-declarations.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Destructuring declarations
Destructuring calls `component1()`, `component2()`, ... on the right-hand side. Data classes generate these in constructor-declaration order.

```kotlin
data class User(val name: String, val age: Int)
val (name, age) = User("Ada", 36)
val (_, onlyAge) = User("Grace", 40)          // underscore skips a component

for ((key, value) in mapOf("a" to 1)) println("$key=$value")   // Map.Entry has component1/2
list.forEachIndexed { i, (n, a) -> println("$i $n $a") }       // lambda parameter

fun minMax(xs: List<Int>): Pair<Int, Int> = xs.min() to xs.max()
val (lo, hi) = minMax(listOf(3, 1, 2))
```

- Any class can opt in by defining `operator fun componentN()`.
- `componentN()` functions must be marked `operator`. The standard library supplies `component1()`/`component2()` for `Map.Entry`, and `Pair` works too.
- With `_`, the `componentN()` function for the skipped component is not called.
- Name-based destructuring (`-Xname-based-destructuring` compiler option) is Experimental; plain destructuring is positional.

Gotcha: destructuring is positional, so reordering constructor parameters in a data class silently swaps values of the same type (`Int, Int`). Prefer named access for classes with several same-typed properties.

Verify: reorder two same-typed properties in a test class and confirm the destructured values change, then switch to property access in that code path.

## Checked
2026-11-08. Read the Kotlin destructuring declarations page in full and trimmed the skill to what it confirms.
Method: documentation only; no commands were run.
