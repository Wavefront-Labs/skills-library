---
id: computing-software.software-engineering.swift.swift-enum-associated-values
name: swift-enum-associated-values
category: computing-software
field: software-engineering
product: swift
tags: [swift, swift-types, enum-associated-values]
level: practitioner
status: docs-checked
description: "Model alternatives with enums carrying data and match them exhaustively with switch."
sources: ["https://docs.swift.org/swift-book/", "https://www.swift.org/documentation/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Enums with associated values and pattern matching
- `enum Result { case ok(Int); case failure(Error) }`; `switch r { case .ok(let v): ...; case .failure(let e): ... }` must be exhaustive.
- `indirect enum` for recursive structures; `CaseIterable` for `allCases`; raw values via `enum E: String`.
Verify: add a case and confirm the compiler flags every switch.

## Checked
2026-11-02. Confirmed: TSPL Enumerations chapter: associated values, exhaustive switch, indirect, CaseIterable and allCases, raw values.
Removed: @unknown default bullet (covered in a chapter not read).
Method: documentation only; no commands were run.
