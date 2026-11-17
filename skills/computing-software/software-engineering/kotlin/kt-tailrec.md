---
id: computing-software.software-engineering.kotlin.kt-tailrec
name: kt-tailrec
category: computing-software
field: software-engineering
product: kotlin
tags: [kotlin, kt-functions, tailrec]
level: intro
status: docs-checked
description: "Use the tailrec modifier so tail-recursive Kotlin functions compile to loops, and know when the compiler rejects it."
sources: ["https://kotlinlang.org/docs/functions.html#tail-recursive-functions"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tail recursive functions
`tailrec` asks the compiler to rewrite a self-recursive function into a loop, avoiding stack growth.

```kotlin
tailrec fun gcd(a: Long, b: Long): Long = if (b == 0L) a else gcd(b, a % b)

tailrec fun sum(xs: List<Int>, i: Int = 0, acc: Long = 0): Long =
    if (i == xs.size) acc else sum(xs, i + 1, acc + xs[i])
```

Conditions:
- The recursive call must be the last operation: nothing may happen after it (`1 + f(n-1)` and `f(n-1) * n` do not qualify).
- It cannot be used inside `try/catch/finally` blocks.
- The function must not be `open`.

Gotcha: `tailrec` applies only when the formal conditions hold; do not assume a function is loop-optimised unless it meets them.

Verify: call `sum(List(1_000_000) { 1 })` and confirm it returns 1000000 without a stack overflow.

## Checked
2026-11-08. Read the Kotlin functions page section on tail recursive functions in full and trimmed the skill to what it confirms.
Method: documentation only; no commands were run.
