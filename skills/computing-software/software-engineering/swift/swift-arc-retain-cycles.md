---
id: computing-software.software-engineering.swift.swift-arc-retain-cycles
name: swift-arc-retain-cycles
category: computing-software
field: software-engineering
product: swift
tags: [swift, swift-memory, arc-retain-cycles]
level: practitioner
status: docs-checked
description: "Find and break retain cycles using weak and unowned references."
sources: ["https://docs.swift.org/swift-book/", "https://www.swift.org/documentation/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ARC retain cycles weak and unowned
- ARC frees a class instance when its strong count reaches zero; two objects holding strong references to each other leak.
- Use `weak` when the other instance has a shorter lifetime: the reference is optional and ARC sets it to nil when the instance is freed.
- Use `unowned` only when the other instance has the same or a longer lifetime: it is expected to always have a value, and accessing it after the instance is freed is a runtime error.
- Closures that capture self can also form strong reference cycles; capture lists break them.
- A `deinit` that prints shows whether an instance was freed.
Verify: assert a weak reference is nil after releasing the owner.

## Checked
2026-11-03. Confirmed against the Swift Programming Language book (swiftlang/swift-book source): AutomaticReferenceCounting chapter (strong reference cycles, weak set to nil, unowned runtime error, deinit) and Closures chapter (capture lists break closure cycles).
Removed: class-bound protocol note, delegate and parent-pointer claim, Xcode Memory Graph and Instruments Leaks.
Method: documentation only; no commands were run.
