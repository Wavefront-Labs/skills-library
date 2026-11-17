---
id: computing-software.software-engineering.swift.swift-closure-capture
name: swift-closure-capture
category: computing-software
field: software-engineering
product: swift
tags: [swift, swift-closures, closure-capture]
level: practitioner
status: docs-checked
description: "Control closure capture with capture lists, @escaping and weak or unowned captures."
sources: ["https://docs.swift.org/swift-book/", "https://www.swift.org/documentation/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Closures capture lists and escaping
- A closure captures constants and variables from its surrounding scope with strong references; closures are reference types.
- A capture list is written before the parameters, requires `in`, and its entries are initialised when the closure is created, each as a constant copy of the same-named variable.
- Weak and unowned captures: `{ [weak self] in print(self!.title) }`, `{ [unowned self] in print(self.title) }`.
- `@escaping` marks a closure parameter that may be called after the function returns, for example when stored outside the function.
- A function call can include multiple trailing closures; the first one drops its argument label.
Verify: release the closure's owner and confirm its deinit runs.

## Checked
2026-11-03. Confirmed against the Swift Programming Language book (swiftlang/swift-book source): Closures chapter (reference types, escaping, trailing closures) and Expressions reference (capture lists, weak and unowned examples).
Removed: guard let self example and Xcode Debug Memory Graph.
Method: documentation only; no commands were run.
