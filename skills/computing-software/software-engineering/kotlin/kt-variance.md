---
id: computing-software.software-engineering.kotlin.kt-variance
name: kt-variance
category: computing-software
field: software-engineering
product: kotlin
tags: [kotlin, kt-generics, variance]
level: advanced
status: docs-checked
description: "Apply out and in variance, and use-site projections, to make generic APIs substitutable."
sources: ["https://kotlinlang.org/docs/generics.html", "https://kotlinlang.org/docs/arrays.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Declaration-site variance in and out
- `interface Source<out T>` marks T as produced only (covariant), so a `Source<String>` can be used where a `Source<Any>` is expected; `in T` (consumer) reverses this.
- Use-site variance: project the type at the use site, e.g. `Array<out Any>` for reading.
- Star projection `Foo<*>` stands for an unknown type: reading gives `Any?`, and writing is not allowed.
- Mnemonic: producer-out, consumer-in (Java's PECS is Producer-Extends, Consumer-Super).
Verify: the compiler rejects a type parameter declared `out` that is used in an `in` position.

## Checked
2026-11-03. Confirmed on the generics page (Source<out T>, star projections, PECS) and the arrays page (Array<out Any>).
Removed: the claim that `List` is covariant and `MutableList` invariant, the `Array<in Any>` example and the exact compiler error message (not on the pages).
Method: documentation only; no commands were run.
