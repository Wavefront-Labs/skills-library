---
id: computing-software.software-engineering.swift.swift-swiftlint-swift-format
name: swift-swiftlint-swift-format
category: computing-software
field: software-engineering
product: swift
tags: [swift, swift-spm, swiftlint-swift-format]
level: practitioner
status: draft
description: "Enforce Swift style with SwiftLint rules and the swift-format tool."
sources: ["https://docs.swift.org/swift-book/", "https://www.swift.org/documentation/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Linting and formatting with SwiftLint and swift-format
- SwiftLint configured in `.swiftlint.yml` (`disabled_rules`, `opt_in_rules`, `excluded`); `swiftlint --fix` auto-corrects; run as a build phase or SwiftPM plugin.
- swift-format (`swift format lint|format`, config `.swift-format` JSON) ships with recent toolchains.
- Pick one formatter per repo to avoid fights; run in CI with `--strict`.
Verify: a deliberate violation fails the CI job.
