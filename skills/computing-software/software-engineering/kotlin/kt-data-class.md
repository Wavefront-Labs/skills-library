---
id: computing-software.software-engineering.kotlin.kt-data-class
name: kt-data-class
category: computing-software
field: software-engineering
product: kotlin
tags: [kotlin, kt-classes, data-class]
level: intro
status: docs-checked
description: "Model value objects with data classes and understand generated members and their pitfalls."
sources: ["https://kotlinlang.org/docs/home.html", "https://kotlinlang.org/spec/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Data classes and copy semantics
- `data class User(val id: Long, val name: String)` generates `equals`, `hashCode`, `toString`, `copy`, `componentN` from primary-constructor properties only.
- Properties declared in the body are ignored by those members.
- `copy` is shallow; mutable collections inside remain shared.
- Prefer `val` properties.
Verify: test that `copy(...)` leaves the original unchanged and equality compares only constructor properties.

## Checked
2026-11-02. Confirmed: kotlinlang.org/docs/data-classes.html: generated members from primary-constructor properties, body properties excluded, copy() shallow.
Removed: JPA entity advice (not in the page).
Method: documentation only; no commands were run.
