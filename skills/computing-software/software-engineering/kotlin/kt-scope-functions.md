---
id: computing-software.software-engineering.kotlin.kt-scope-functions
name: kt-scope-functions
category: computing-software
field: software-engineering
product: kotlin
tags: [kotlin, kt-functions, scope-functions]
level: practitioner
status: docs-checked
description: "Pick among let, run, with, apply and also by receiver reference and return value."
sources: ["https://kotlinlang.org/docs/scope-functions.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Scope functions let run with apply also
- `let` (`it`, returns the lambda result) suits null-checks and transforms. `run` (`this`, lambda result) computes a value with a receiver. `with(obj) {}` (`this`, lambda result) is the non-extension form.
- `apply` (`this`, returns the object) configures an object. `also` (`it`, returns the object) suits side effects like logging.
- Avoid nesting scope functions and be careful chaining them: it is easy to lose track of the current `this` or `it`.
- Do not use them just to save a variable name.
Verify: if you cannot say why the return value matters, use plain statements.

## Checked

Date: 2026-11-02. Confirmed on kotlinlang.org docs (scope-functions.html): receiver reference (this or it) and return value of let, run, with, apply, also; advice to avoid nesting and overuse. Removed as not stated there: the 'two levels' nesting limit.

Method: documentation only; no commands were run.
