---
id: computing-software.software-engineering.kotlin.kt-smart-cast
name: kt-smart-cast
category: computing-software
field: software-engineering
product: kotlin
tags: [kotlin, kt-null-safety, smart-cast]
level: practitioner
status: docs-checked
description: "Rely on smart casts after is/null checks and avoid the cases where the compiler refuses them."
sources: ["https://kotlinlang.org/docs/typecasts.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Smart casts and their limits
- After `if (x is String)` or `if (x != null)` the compiler treats `x` as the narrower type in that scope; it also works for `when` branches.
- Smart casts work on `val` locals (except local delegated properties), `var` locals not modified between check and use and not captured in a lambda that modifies them, and `val` properties that are `private` or `internal` or checked in the module that declares them.
- They do not work on `var` properties, `open` properties, or properties with custom getters: copy to a local `val` first (`val v = this.v ?: return`).
Verify: when the compiler refuses a smart cast, copy the value to a local `val`.

## Checked

Date: 2026-11-02. Confirmed on kotlinlang.org docs (typecasts.html): smart cast conditions for val/var locals, val/var properties, open and custom-getter properties, when. Removed as not stated there: the exact error message text and 'another module' wording.

Method: documentation only; no commands were run.
