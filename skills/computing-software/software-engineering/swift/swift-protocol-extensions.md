---
id: computing-software.software-engineering.swift.swift-protocol-extensions
name: swift-protocol-extensions
category: computing-software
field: software-engineering
product: swift
tags: [swift, swift-protocols, protocol-extensions]
level: practitioner
status: docs-checked
description: "Design with protocols and extensions: default implementations, conditional conformance and protocol composition."
sources: ["https://docs.swift.org/swift-book/", "https://www.swift.org/documentation/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Protocols extensions and default implementations
- A protocol can be extended to implement some of its requirements as default implementations.
- Swift reports a compile-time error if a conforming type doesn't fulfil a protocol requirement.
- Conditional conformance: `extension Array: TextRepresentable where Element: TextRepresentable`.
- Protocol composition: `typealias PQ = P & Q`.
Verify: remove a required member from a conforming type and confirm the compiler reports it.

## Checked
2026-11-03. Confirmed against the Swift Programming Language book (swiftlang/swift-book source): Protocols chapter (requirements, extensions, conditional conformance) and Types reference (protocol composition).
Removed: static versus dynamic dispatch claims (not in the book).
Method: documentation only; no commands were run.
