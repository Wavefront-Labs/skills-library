---
id: computing-software.software-engineering.kotlin.kt-typealias
name: kt-typealias
category: computing-software
field: software-engineering
product: kotlin
tags: [kotlin, kt-generics, typealias]
level: intro
status: docs-checked
description: "Use typealias to name function types and long generics, knowing it creates no new type."
sources: ["https://kotlinlang.org/docs/type-aliases.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Type aliases and typealias limits
- `typealias RequestHandler = (Request) -> Response` and `typealias UserIndex = Map<Long, User>` give shorter names to function types and long generic types.
- A type alias doesn't create a new type, so it is interchangeable with its target and gives no extra type safety (use a value class for that).
- Declare aliases at the top level.
Verify: pass the underlying type where the alias is expected and confirm it compiles.

## Checked
2026-11-03. Confirmed on the Kotlin type aliases page: function-type and generic aliases, "doesn't create a new type", top-level declaration.
Removed: nothing; examples replaced with ones taken from the page.
Method: documentation only; no commands were run.
