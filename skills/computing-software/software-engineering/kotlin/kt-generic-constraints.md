---
id: computing-software.software-engineering.kotlin.kt-generic-constraints
name: kt-generic-constraints
category: computing-software
field: software-engineering
product: kotlin
tags: [kotlin, kt-generics, generic-constraints]
level: practitioner
status: docs-checked
description: "Constrain type parameters with : bounds and where clauses, and understand definitely non-null types."
sources: ["https://kotlinlang.org/docs/generics.html", "https://kotlinlang.org/docs/inline-functions.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Upper bounds and where clauses
- One upper bound goes after the colon: `fun <T : Comparable<T>> max(a: T, b: T): T`. For several bounds use a `where` clause: `where T : CharSequence, T : Comparable<T>`; the type must satisfy all of them.
- The default upper bound is `Any?`. Declare a definitely non-nullable type with `T & Any` (the type parameter must have a nullable upper bound).
- Generic type arguments are erased at run time: you cannot check `is List<Int>`, but you can check against a star-projected type such as `is List<*>`. An `inline` function with a `reified` type parameter keeps the type at run time.
Verify: compile a call with a violating argument to confirm the bound.

## Checked
2026-11-03. Confirmed on the generics and inline functions pages: upper bounds, where clauses with multiple bounds, default bound Any?, definitely non-nullable T & Any, type erasure and star-projection checks, reified.
Removed: "since Kotlin 1.7" (version not on the page).
Method: documentation only; no commands were run.
