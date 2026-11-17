---
id: computing-software.software-engineering.kotlin.kt-enum-classes
name: kt-enum-classes
category: computing-software
field: software-engineering
product: kotlin
tags: [kotlin, kt-classes, enum-classes]
level: intro
status: docs-checked
description: "Model fixed sets with Kotlin enum classes: properties, abstract members, entries, valueOf and use in when."
sources: ["https://kotlinlang.org/docs/enum-classes.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Enum classes
```kotlin
enum class Protocol(val port: Int) {
    HTTP(80), HTTPS(443);
    fun secure() = this == HTTPS
}

enum class State {
    IDLE { override fun next() = RUNNING },
    RUNNING { override fun next() = IDLE };
    abstract fun next(): State
}

val p = Protocol.valueOf("HTTPS")      // throws IllegalArgumentException if no match
val all = Protocol.entries             // a specialized List of all constants
val label = when (p) { Protocol.HTTP -> "plain"; Protocol.HTTPS -> "tls" }  // all constants used: no else needed
```

- Constants are separated by commas; a semicolon is required before any members.
- Each constant is an object and may override abstract members via an anonymous body.
- `name` and `ordinal` are built in; do not persist `ordinal`, since reordering entries changes it. Persist `name` or an explicit code property.
- `entries` is a specialized `List`, so `entries.getOrNull(i)`, `first { }` and `sorted()` work; `sorted()` and `<` follow declaration order (`ordinal`) and `compareTo` cannot be overridden.
- In generic code use `enumEntries<T>()` (recommended; every call returns the same list), `enumValueOf<T>()` (throws `IllegalArgumentException` on no match) or `enumValues<T>()` (new array per call).
- An enum class can implement interfaces but cannot inherit from a class.

Gotcha: need subtypes with differing data per case? Use a sealed class or interface instead; enums have one shape of state for all constants.

Verify: call `valueOf("nope")` in a test and expect `IllegalArgumentException`; `entries.getOrNull(99)` returns null.

## Checked
2026-11-08. Read the Kotlin enum classes page in full and trimmed the skill to what it confirms.
Method: documentation only; no commands were run.
