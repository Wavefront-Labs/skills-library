---
id: computing-software.software-engineering.swift.swift-some-any-types
name: swift-some-any-types
category: computing-software
field: software-engineering
product: swift
tags: [swift, swift-protocols, some-any-types]
level: advanced
status: docs-checked
description: "Choose between some P (opaque) and any P (boxed protocol) types."
sources: ["https://docs.swift.org/swift-book/", "https://www.swift.org/documentation/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Opaque some and existential any types
- `some P`: an opaque type that refers to one specific type; the underlying type's identity is preserved, and all possible return values must have the same type.
- `any P`: a boxed protocol (existential) type that can hold different conforming types, for example `var shapes: [any Shape]`.
- A protocol with associated types used as a type must be written `any Container`; return `some Container` for an opaque result.
- Returning different types from branches fails with `some`; use `any`.
Verify: switch a function from any to some and look at the compile errors.

## Checked
2026-11-03. Confirmed against the Swift Programming Language book (swiftlang/swift-book source): OpaqueTypes chapter.
Removed: SwiftUI some View remark, ExistentialAny SE-0335 note, AnyView erasure and cost claims.
Method: documentation only; no commands were run.
