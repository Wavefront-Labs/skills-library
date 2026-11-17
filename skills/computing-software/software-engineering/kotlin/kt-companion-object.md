---
id: computing-software.software-engineering.kotlin.kt-companion-object
name: kt-companion-object
category: computing-software
field: software-engineering
product: kotlin
tags: [kotlin, kt-classes, companion-object]
level: practitioner
status: docs-checked
description: "Use object, companion object and const/@JvmStatic correctly for singletons and factories."
sources: ["https://kotlinlang.org/docs/home.html", "https://kotlinlang.org/spec/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Object declarations and companion objects
- `object Registry { }` is a thread-safe lazily initialised singleton; `companion object { fun create() = ... }` holds class-level members, can implement interfaces.
- On the JVM, `@JvmStatic` generates real static methods and fields for companion members.
- Singletons with mutable state are global state: prefer dependency injection in testable code.
Verify: call from Java to confirm the static/instance form you intended.

## Checked
2026-11-02. Confirmed: kotlinlang.org/docs/object-declarations.html: object declarations thread-safe and lazily initialised on first access, companion objects hold class-level members and can implement interfaces, @JvmStatic.
Removed: const val rules and @JvmField (not in the page).
Method: documentation only; no commands were run.
