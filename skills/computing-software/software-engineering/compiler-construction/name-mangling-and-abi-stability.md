---
id: computing-software.software-engineering.compiler-construction.name-mangling-and-abi-stability
name: name-mangling-and-abi-stability
category: computing-software
field: software-engineering
product: compiler-construction
tags: [compiler-construction, name-mangling, itanium-abi, abi-versioning, compilers, interpreters, language-implementation]
level: practitioner
status: draft
description: "Symbol naming"
sources: ["https://craftinginterpreters.com/", "https://llvm.org/docs/", "https://llvm.org/docs/tutorial/", "https://mlir.llvm.org/docs/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Name mangling and ABI stability

Goal: keep binaries compatible.
- Itanium mangling encodes namespaces and parameter types; Rust v0 and legacy schemes differ; `extern "C"` disables mangling.
- ABI breaks: layout, vtable and inline changes.
- Check with `nm -C`, `abidiff`.
Verify: libraries link across compiler versions.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
