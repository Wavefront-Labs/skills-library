---
id: computing-software.software-engineering.swift.swift-swift-testing-framework
name: swift-swift-testing-framework
category: computing-software
field: software-engineering
product: swift
tags: [swift, swift-testing, swift-testing-framework]
level: practitioner
status: draft
description: "Use the Swift Testing macros @Test, #expect and parameterised tests (Swift 6 toolchains)."
sources: ["https://docs.swift.org/swift-book/", "https://www.swift.org/documentation/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Swift Testing framework
- `import Testing`; `@Test func sums() { #expect(add(1,2) == 3) }`; `#require` unwraps/throws; `@Test(arguments: [1,2,3])` parameterised; `@Suite` groups; traits like `.tags()` and `.disabled()`.
- Runs in parallel by default; can coexist with XCTest in one target. Ships with Xcode 16 / Swift 6 toolchains.
Verify: `swift test` lists both frameworks' results.
