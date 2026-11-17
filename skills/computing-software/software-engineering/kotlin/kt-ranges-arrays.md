---
id: computing-software.software-engineering.kotlin.kt-ranges-arrays
name: kt-ranges-arrays
category: computing-software
field: software-engineering
product: kotlin
tags: [kotlin, kt-collections, ranges-arrays]
level: intro
status: docs-checked
description: "Iterate with ranges and progressions and choose between arrays and lists."
sources: ["https://kotlinlang.org/docs/ranges.html", "https://kotlinlang.org/docs/arrays.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Ranges, progressions and arrays
- `1..10`, `10 downTo 1`, `1..10 step 2`; `..<` creates an exclusive upper bound (via `rangeUntil()`).
- `Array<T>` is invariant: `Array<String>` is not a subtype of `Array<Any>`. Primitive-type arrays (`IntArray`, `LongArray`) store values without boxing; `toTypedArray()` converts them to object arrays.
Verify: IntArray vs Array<Int> allocation shows in a heap profile.

## Checked

Date: 2026-11-02. Confirmed on kotlinlang.org docs (ranges.html, arrays.html): ..<, downTo, step, array invariance, primitive-type arrays without boxing, toTypedArray. Removed as not stated there: the Kotlin 1.9 stability claim, `1 until 10`, `arrayOf` specifics and withIndex advice (not read).

Method: documentation only; no commands were run.
