---
id: computing-software.software-engineering.kotlin.kt-readonly-collections
name: kt-readonly-collections
category: computing-software
field: software-engineering
product: kotlin
tags: [kotlin, kt-collections, readonly-collections]
level: practitioner
status: docs-checked
description: "Understand that List is a read-only view, not immutable, and copy defensively at boundaries."
sources: ["https://kotlinlang.org/docs/collections-overview.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Read-only vs mutable collections
- Each collection type (`List`, `Set`, `Map`) has a read-only interface for access and a mutable interface (`MutableList` etc.) that adds adding, removing and updating.
- Return a copy from classes that own mutable state rather than the mutable instance.
Verify: cast to `MutableList` in a test to prove a leak, then fix with a copy.

## Checked

Date: 2026-11-02. Confirmed on kotlinlang.org docs (collections-overview.html): read-only vs mutable interface pairs. Removed as not stated there: claims about backing by mutable lists, toList(), and kotlinx.collections.immutable (not read).

Method: documentation only; no commands were run.
