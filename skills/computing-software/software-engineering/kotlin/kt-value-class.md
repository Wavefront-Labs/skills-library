---
id: computing-software.software-engineering.kotlin.kt-value-class
name: kt-value-class
category: computing-software
field: software-engineering
product: kotlin
tags: [kotlin, kt-classes, value-class]
level: advanced
status: docs-checked
description: "Wrap primitives with @JvmInline value classes for type safety, and know the boxing and name-mangling cases."
sources: ["https://kotlinlang.org/docs/inline-classes.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Value classes
- `@JvmInline value class UserId(val raw: Long)` is a distinct type at compile time; on the JVM it is normally represented by the underlying value (unboxed).
- It needs a single property initialised in the primary constructor, cannot have backing fields, has no identity, and may implement interfaces.
- It is boxed when used as another type: as a generic type argument, as an interface type, or when nullable.
- Functions that take value classes are mangled with a stable hash in the JVM name, which affects Java callers; `@JvmName` can disable the mangling.
Verify: check bytecode for boxing in hot paths before claiming a performance win.

## Checked
2026-11-03. Confirmed on the inline classes page: single constructor property, no backing fields, no identity, interfaces, boxing cases, name mangling and @JvmName.
Removed: "no var" wording (replaced with the page's no-backing-fields rule).
Method: documentation only; no commands were run.
