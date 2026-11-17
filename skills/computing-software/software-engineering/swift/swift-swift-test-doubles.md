---
id: computing-software.software-engineering.swift.swift-swift-test-doubles
name: swift-swift-test-doubles
category: computing-software
field: software-engineering
product: swift
tags: [swift, swift-testing, swift-test-doubles]
level: practitioner
status: draft
description: "Make Swift code testable with protocol-based injection and simple fakes."
sources: ["https://docs.swift.org/swift-book/", "https://www.swift.org/documentation/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Dependency injection and test doubles in Swift
- Inject dependencies via initialisers typed as protocols (`any Clock`, `URLSessionProtocol`) with production defaults.
- Prefer hand-written fakes/stubs; Swift lacks runtime mocking so mock libraries are code-generated.
- Inject time (`Clock` protocol / `ContinuousClock`) and randomness for determinism.
Verify: tests run without network or file system.
