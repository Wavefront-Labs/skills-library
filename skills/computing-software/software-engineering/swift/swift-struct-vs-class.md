---
id: computing-software.software-engineering.swift.swift-struct-vs-class
name: swift-struct-vs-class
category: computing-software
field: software-engineering
product: swift
tags: [swift, swift-types, struct-vs-class]
level: practitioner
status: docs-checked
description: "Choose between struct and class by value versus reference semantics and identity."
sources: ["https://docs.swift.org/swift-book/", "https://www.swift.org/documentation/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Structs vs classes and copy semantics
- Structs and enums are value types (copied on assignment); classes are reference types with identity (`===`), inheritance and deinit.
- Prefer struct unless you need shared mutable identity: two names for a class instance refer to the same instance, which can be harder to reason about.
- Arrays and dictionaries are value types; their elements are copied just before a modification.
- Classes don't receive a default memberwise initialiser; structs do.
Verify: mutate a copy in a test and assert the original is unchanged.

## Checked
2026-11-03. Confirmed against the Swift Programming Language book (swiftlang/swift-book source): ClassesAndStructures chapter.
Removed: Objective-C and framework advice, struct-holding-class sharing claim and let semantics bullet (not in the chapter).
Method: documentation only; no commands were run.
