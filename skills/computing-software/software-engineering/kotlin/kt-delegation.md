---
id: computing-software.software-engineering.kotlin.kt-delegation
name: kt-delegation
category: computing-software
field: software-engineering
product: kotlin
tags: [kotlin, kt-classes, delegation]
level: advanced
status: docs-checked
description: "Use class delegation with by and property delegates (lazy, observable, map) correctly."
sources: ["https://kotlinlang.org/docs/delegation.html", "https://kotlinlang.org/docs/delegated-properties.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Delegation and delegated properties
- `class Logged(impl: Repo) : Repo by impl` delegates the interface's public members to `impl`; you may override members.
- Standard property delegates: `by lazy`, `Delegates.observable(initial) { prop, old, new -> }`, `Delegates.vetoable` (the handler runs before assignment and can veto), and storing properties in a map.
- A custom delegate provides `operator fun getValue(thisRef, property)` and, for `var`, `setValue`; it need not implement an interface.
- The compiler generates auxiliary properties for some delegates, so keep delegates cheap.
Verify: unit test that observable callbacks fire once per assignment.

## Checked

Date: 2026-11-02. Confirmed on kotlinlang.org docs (delegation.html, delegated-properties.html): class delegation by, lazy/observable/vetoable/map, getValue/setValue operator, auxiliary properties. Removed as not stated there: the 'hidden field' wording.

Method: documentation only; no commands were run.
