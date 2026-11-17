---
id: computing-software.software-engineering.kotlin.kt-sealed-class
name: kt-sealed-class
category: computing-software
field: software-engineering
product: kotlin
tags: [kotlin, kt-classes, sealed-class]
level: practitioner
status: docs-checked
description: "Model closed hierarchies with sealed classes/interfaces and exhaustive when expressions."
sources: ["https://kotlinlang.org/docs/sealed-classes.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sealed classes and exhaustive when
- `sealed interface Result { data class Ok(val v: Int): Result; data object Err: Result }` restricts direct subtypes to the same package (and, for interfaces, the same module).
- `when (r) { is Result.Ok -> ...; Result.Err -> ... }` over a sealed type is checked for exhaustiveness, so no `else` is needed; adding a subtype then breaks compilation where handling is missing. Do not add an `else` that hides this.
- In common multiplatform code, a `when` on an expected sealed class still needs an `else` branch.
Verify: add a new subtype and confirm the compiler flags every `when`.

## Checked

Date: 2026-11-02. Confirmed on kotlinlang.org docs (sealed-classes.html): same-package/module rule, exhaustive when without else, data object syntax, expected-sealed-class else. Removed as not stated there: the Kotlin 1.9 version gate for data object (the page does not state it).

Method: documentation only; no commands were run.
