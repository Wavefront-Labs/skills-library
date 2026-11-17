---
id: computing-software.software-engineering.swift.swift-initialisers
name: swift-initialisers
category: computing-software
field: software-engineering
product: swift
tags: [swift, swift-types, initialisers]
level: practitioner
status: docs-checked
description: "Write designated, convenience and failable initialisers, respecting two-phase init rules."
sources: ["https://docs.swift.org/swift-book/", "https://www.swift.org/documentation/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Initialisers and two-phase initialisation
- Classes: designated initialiser must initialise all own properties, then call super.init; convenience initialisers delegate across (`self.init`). Structs get a memberwise initialiser unless you define one in the main declaration (put custom inits in an extension to keep it).
- Failable: `init?(raw: String)` returns nil.
- `required init` for subclass obligations.
Verify: the compiler rejects use of `self` before initialisation is complete.

## Checked
2026-11-02. Confirmed: TSPL Initialization chapter: designated and convenience initialisers, memberwise initialiser and the extension tip, failable init?, required.
Removed: Throwing-initialiser bullet and the quoted compiler message (not in the chapter).
Method: documentation only; no commands were run.
