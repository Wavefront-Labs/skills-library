---
id: computing-software.software-engineering.kotlin.kt-dsl-builders
name: kt-dsl-builders
category: computing-software
field: software-engineering
product: kotlin
tags: [kotlin, kt-dsl, dsl-builders]
level: advanced
status: docs-checked
description: "Design DSLs with lambdas with receiver and @DslMarker to stop receiver leakage."
sources: ["https://kotlinlang.org/docs/type-safe-builders.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Lambdas with receiver and DSL markers
- A builder function takes a lambda with receiver, e.g. `fun html(init: Html.() -> Unit): Html`, so `this` inside the block is the builder.
- Without protection an inner block can call members of an outer implicit receiver (for example a `head` tag inside another `head`). Annotate the builder classes with a custom annotation marked `@DslMarker`; implicit receivers of the same DSL then only allow calling members of the nearest receiver.
- The marker can also be applied directly to function types, which needs `AnnotationTarget.TYPE` among the annotation targets.
- Keep DSLs for configuration trees; avoid them for ordinary logic.
Verify: a nested block calling an outer-receiver member fails to compile.

## Checked
2026-11-03. Confirmed on the type-safe builders page: lambdas with receiver, the implicit-receiver leak, @DslMarker behaviour, AnnotationTarget.TYPE for function types.
Removed: nothing.
Method: documentation only; no commands were run.
