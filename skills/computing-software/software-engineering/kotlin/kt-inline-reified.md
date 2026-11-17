---
id: computing-software.software-engineering.kotlin.kt-inline-reified
name: kt-inline-reified
category: computing-software
field: software-engineering
product: kotlin
tags: [kotlin, kt-functions, inline-reified]
level: advanced
status: docs-checked
description: "Use inline functions to remove lambda allocation and enable reified type parameters."
sources: ["https://kotlinlang.org/docs/inline-functions.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Inline, noinline and crossinline
- `inline fun <T> measure(block: () -> T): T` inlines the function and its lambda arguments at call sites; a bare `return` normally cannot exit from inside a lambda, but inlined lambdas may use non-local returns.
- `noinline` marks lambda parameters that must not be inlined; `crossinline` marks a lambda that cannot use non-local returns.
- The compiler warns when an inline function has no inlinable function parameters and no reified type parameters, since inlining it is unlikely to help.
- Public or protected inline functions that are not part of a private/internal declaration have restrictions for API compatibility; read that section before exposing one.
Verify: check that the compiler emits no inline warning for your function.

## Checked

Date: 2026-11-02. Confirmed on kotlinlang.org docs (inline-functions.html): inline, noinline, crossinline, non-local returns, the no-benefit warning, public-API restrictions. Removed as not stated there: reified runtime-use examples (T::class, is T), the IDE bytecode menu path and the ABI wording.

Method: documentation only; no commands were run.
