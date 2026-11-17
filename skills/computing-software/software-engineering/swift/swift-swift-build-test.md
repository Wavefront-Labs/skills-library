---
id: computing-software.software-engineering.swift.swift-swift-build-test
name: swift-swift-build-test
category: computing-software
field: software-engineering
product: swift
tags: [swift, swift-spm, swift-build-test]
level: practitioner
status: draft
description: "Build and test from the CLI with debug/release configurations, filters and parallelism."
sources: ["https://docs.swift.org/swift-book/", "https://www.swift.org/documentation/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Build configurations and swift test
- `swift build -c release`, `swift test --filter MyTests/testFoo`, `swift test --parallel`, `--enable-code-coverage`.
- `swift package clean` / `reset`, `swift package update`, `swift package show-dependencies`.
- Compiler flags via `swiftSettings: [.unsafeFlags([...])]` (blocks use as a dependency); prefer `.enableUpcomingFeature("...")`.
Verify: CI builds both debug and release; optimisation changes can expose UB-adjacent bugs.
