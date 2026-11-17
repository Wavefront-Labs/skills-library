---
id: computing-software.software-engineering.kotlin.kt-java-property-access
name: kt-java-property-access
category: computing-software
field: software-engineering
product: kotlin
tags: [kotlin, kt-java-interop, java-property-access]
level: intro
status: docs-checked
description: "Use Kotlin property syntax for Java getters/setters and handle keyword-named Java members."
sources: ["https://kotlinlang.org/docs/java-interop.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Java getters setters and property syntax
- Java no-argument `getX()` and single-argument `setX(v)` methods are seen as the synthetic property `x`. Boolean accessors (getter starting with `is`, setter with `set`) become a property with the same name as the getter, e.g. `isLenient`.
- A getter that takes parameters does not become a property. A Java class with only a setter shows no property, because Kotlin has no set-only properties.
- Java identifiers that are Kotlin keywords (`in`, `object`, `is` and others) are called by escaping with backticks: ``foo.`is`(bar)``.
Verify: compile against the Java class; an unresolved reference means the getter pattern did not match.

## Checked
2026-11-03. Confirmed on the Java interop page: synthetic properties, boolean accessors, set-only limitation, backtick escaping.
Removed: the Java records claim (not covered by the page read).
Method: documentation only; no commands were run.
