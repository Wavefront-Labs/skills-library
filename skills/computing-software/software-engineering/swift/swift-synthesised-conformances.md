---
id: computing-software.software-engineering.swift.swift-synthesised-conformances
name: swift-synthesised-conformances
category: computing-software
field: software-engineering
product: swift
tags: [swift, swift-protocols, synthesised-conformances]
level: intro
status: docs-checked
description: "Rely on compiler-synthesised Equatable, Hashable and Comparable, and know when synthesis does not apply."
sources: ["https://docs.swift.org/swift-book/", "https://www.swift.org/documentation/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Equatable Hashable Comparable Codable conformances
- Equatable and Hashable are synthesised for structs whose stored properties all conform, enums whose associated types all conform, and enums with no associated types. Declare the conformance in the file with the original declaration and don't implement `==` or `hash(into:)` yourself.
- Comparable is synthesised for enums without a raw value; any associated types must be Comparable. An enum with a raw type such as `enum E: Int, Comparable` doesn't get it.
Verify: add the conformance without writing `==` or `<` and confirm the code compiles.

## Checked
2026-11-03. Confirmed against the Swift Programming Language book (swiftlang/swift-book source): Protocols chapter, Synthesized Implementation.
Removed: Codable, CodingKeys and JSONDecoder strategies (not in the book), consistency remark and the associated-values restriction on Comparable (the book allows Comparable associated types).
Method: documentation only; no commands were run.
