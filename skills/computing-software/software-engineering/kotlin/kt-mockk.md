---
id: computing-software.software-engineering.kotlin.kt-mockk
name: kt-mockk
category: computing-software
field: software-engineering
product: kotlin
tags: [kotlin, kt-testing, mockk]
level: practitioner
status: docs-checked
description: "Mock Kotlin classes and suspend functions with MockK, using every, coEvery and verify."
sources: ["https://github.com/mockk/mockk"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MockK mocking
- `mockk<Type>()` creates a mock; stub with `every { ... } returns value`; for suspend functions use `coEvery { ... }` and `coVerify { ... }`.
- `relaxed = true` makes unstubbed calls return simple defaults. `mockkStatic` and `mockkObject` mock top-level/extension functions and objects; clear them with `unmockkAll()` (or the matching `unmock...`) afterwards.
- Prefer fakes over deep mock chains; verify only behaviour that matters.
Verify: tests fail when the verified call is removed.

## Checked
2026-11-03. Confirmed on the MockK README: mockk<T>(), every, coEvery, coVerify, relaxed = true, mockkStatic, mockkObject, unmockkAll.
Removed: the claim that MockK is needed for "final classes" in the description (not stated in the lines checked).
Method: documentation only; no commands were run.
