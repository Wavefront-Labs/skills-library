---
id: computing-software.software-engineering.swift.swift-string-unicode
name: swift-string-unicode
category: computing-software
field: software-engineering
product: swift
tags: [swift, swift-collections-strings, string-unicode]
level: practitioner
status: docs-checked
description: "Handle Swift strings by grapheme clusters, indices, views and substrings correctly."
sources: ["https://docs.swift.org/swift-book/", "https://www.swift.org/documentation/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# String indices Characters and Unicode
- A `String` is a collection of `Character` values (extended grapheme clusters); `count` must iterate over the whole string to find character boundaries.
- Index with `String.Index`, not Int: `greeting[greeting.startIndex]`, `greeting.index(greeting.startIndex, offsetBy: 7)`.
- Views: `unicodeScalars`, `utf8`, `utf16`.
- A slice such as `greeting[..<index]` is a `Substring`, meant for short-term use; convert with `String(beginning)` to store it longer.
- Strings are equal when their extended grapheme clusters are canonically equivalent.
Verify: test with emoji, combining marks and flags.

## Checked
2026-11-03. Confirmed against the Swift Programming Language book (swiftlang/swift-book source): StringsAndCharacters chapter.
Removed: O(n) wording and storage-sharing claim for Substring (not stated).
Method: documentation only; no commands were run.
