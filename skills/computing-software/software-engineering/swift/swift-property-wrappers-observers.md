---
id: computing-software.software-engineering.swift.swift-property-wrappers-observers
name: swift-property-wrappers-observers
category: computing-software
field: software-engineering
product: swift
tags: [swift, swift-types, property-wrappers-observers]
level: practitioner
status: docs-checked
description: "Use computed, lazy, observed properties and property wrappers appropriately."
sources: ["https://docs.swift.org/swift-book/", "https://www.swift.org/documentation/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Properties observers and lazy properties
- Stored vs computed properties; a `lazy` property must be a `var` because its initial value is computed on first use, after initialisation completes.
- If a lazy property is accessed by several threads before it is initialised, it may not be initialised only once.
- Observers `willSet`/`didSet` are not called while a class sets its own properties in its initialiser.
- Property wrappers (`@propertyWrapper`) define a `wrappedValue`; an optional `projectedValue` is read with a `$` prefix.
Verify: print in observers during init to confirm they do not fire.

## Checked
2026-11-03. Confirmed against the Swift Programming Language book (swiftlang/swift-book source): Properties chapter (lazy, observers, property wrappers, projected values).
Removed: struct mutability remark on lazy, SwiftUI wrapper names and the wrapper cost remark.
Method: documentation only; no commands were run.
