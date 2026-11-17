---
id: computing-software.software-engineering.kotlin.kt-sam-conversion
name: kt-sam-conversion
category: computing-software
field: software-engineering
product: kotlin
tags: [kotlin, kt-java-interop, sam-conversion]
level: practitioner
status: docs-checked
description: "Pass Kotlin lambdas to Java interfaces and declare fun interfaces for Kotlin SAMs."
sources: ["https://kotlinlang.org/docs/java-interop.html", "https://kotlinlang.org/docs/fun-interfaces.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SAM conversions and functional interfaces
- Java interfaces with a single non-default method accept lambdas: `executor.execute { work() }`, or explicitly `Runnable { work() }`. SAM conversion works for interfaces, not abstract classes.
- Kotlin: declare `fun interface Validator { fun validate(s: String): Boolean }` (the `fun` modifier; exactly one abstract member function, other members must be non-abstract) and construct it with a lambda: `Validator { it.isNotBlank() }`.
- Function-type parameters (`(String) -> Boolean`) are usually simpler for Kotlin-only APIs.
Verify: compile a call site with a lambda and a named object to compare.

## Checked
2026-11-03. Confirmed on the Java interop page (SAM conversions, Runnable and executor.execute examples, interfaces only) and the functional interfaces page (fun modifier, single abstract member, lambda construction).
Removed: nothing.
Method: documentation only; no commands were run.
