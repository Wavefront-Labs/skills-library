---
id: computing-software.software-engineering.kotlin.kt-extension-functions
name: kt-extension-functions
category: computing-software
field: software-engineering
product: kotlin
tags: [kotlin, kt-functions, extension-functions]
level: practitioner
status: docs-checked
description: "Write extension functions correctly: static dispatch, member-wins rule and scope."
sources: ["https://kotlinlang.org/docs/extensions.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Extension functions and properties
- `fun String.isEmail(): Boolean = ...` adds call-site syntax; when declared outside the class it cannot access the receiver's private or protected members.
- Extensions are dispatched statically on the declared receiver type, not the runtime type.
- If a member and an extension have the same receiver type, name and compatible arguments, the member wins.
- Nullable receivers: define the extension on `String?` and handle null inside it.
Verify: a unit test calling via a base-typed variable shows static dispatch.

## Checked

Date: 2026-11-02. Confirmed on kotlinlang.org docs (extensions.html): static dispatch, member wins, private-member limit, nullable receivers. Removed as not stated there: import-by-name and file-naming/visibility advice, and the String?.orDash example.

Method: documentation only; no commands were run.
