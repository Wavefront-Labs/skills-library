---
id: computing-software.software-engineering.kotlin.kt-lateinit-lazy
name: kt-lateinit-lazy
category: computing-software
field: software-engineering
product: kotlin
tags: [kotlin, kt-null-safety, lateinit-lazy]
level: practitioner
status: docs-checked
description: "Choose between lateinit var, by lazy and nullable fields for deferred initialisation."
sources: ["https://kotlinlang.org/docs/properties.html", "https://kotlinlang.org/docs/delegated-properties.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# lateinit and lazy initialisation
- `lateinit var x: T` needs a non-nullable, non-primitive type; accessing it before initialisation throws `UninitializedPropertyAccessException`. Check with `::x.isInitialized`.
- `val x by lazy { ... }` computes once on first access; by default evaluation is synchronized. Pass `LazyThreadSafetyMode.PUBLICATION` or `NONE` deliberately.
- `lazy` suits expensive read-only values; `lateinit` suits mutable fields set after construction (DI, tests).
Verify: write a test that accesses the property before init and asserts the failure mode you expect.

## Checked

Date: 2026-11-02. Confirmed on kotlinlang.org docs (properties.html, delegated-properties.html): lateinit constraints and exception, isInitialized, lazy default synchronized, PUBLICATION and NONE. Removed as not stated there: nothing material; the DI/test use-case is advice only.

Method: documentation only; no commands were run.
