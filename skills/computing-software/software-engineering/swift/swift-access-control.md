---
id: computing-software.software-engineering.swift.swift-access-control
name: swift-access-control
category: computing-software
field: software-engineering
product: swift
tags: [swift, swift-api-design, access-control]
level: practitioner
status: docs-checked
description: "Choose among private, fileprivate, internal, package, public and open."
sources: ["https://docs.swift.org/swift-book/", "https://www.swift.org/documentation/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Access control and module boundaries
- Default is `internal`. `public` allows use outside module; `open` also allows subclassing/overriding; `package` shares within a package.
- `private` is lexical scope plus same-file extensions of that type.
- `public` types do not expose internal types in signatures.
Verify: compile a client target against the library.

## Checked
2026-11-02. Confirmed: TSPL AccessControl chapter: internal default, public/open and subclassing, private scope with same-file extensions, package access, public declarations cannot use less-accessible types.
Removed: Swift 5.9 version note and @usableFromInline/@inlinable bullet (not in the chapter).
Method: documentation only; no commands were run.
