---
id: computing-software.software-engineering.compiler-construction.source-maps-and-pdb
name: source-maps-and-pdb
category: computing-software
field: software-engineering
product: compiler-construction
tags: [compiler-construction, source-maps, pdb-files, symbolication, compilers, interpreters, language-implementation]
level: practitioner
status: draft
description: "Other formats"
sources: ["https://craftinginterpreters.com/", "https://llvm.org/docs/", "https://llvm.org/docs/tutorial/", "https://mlir.llvm.org/docs/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Source maps, PDB and symbolication

Goal: map binaries back to source.
- Source maps (JS/Wasm), PDB (Windows), dSYM (macOS); split debug files and build IDs for symbol servers.
- Keep symbols for crash analysis, strip for shipping.
- `addr2line`, `llvm-symbolizer`.
Verify: a crash address resolves to the correct source line.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
