---
id: computing-software.software-engineering.compiler-construction.static-and-dynamic-linking
name: static-and-dynamic-linking
category: computing-software
field: software-engineering
product: compiler-construction
tags: [compiler-construction, ld-script, plt-got, dynamic-loader, compilers, interpreters, language-implementation]
level: practitioner
status: draft
description: "Linking models"
sources: ["https://craftinginterpreters.com/", "https://llvm.org/docs/", "https://llvm.org/docs/tutorial/", "https://mlir.llvm.org/docs/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Static vs dynamic linking and loaders

Goal: understand linking.
- Static archives resolve at link time (order matters); shared libraries via PLT/GOT and lazy binding; `LD_LIBRARY_PATH`, RPATH/RUNPATH.
- Linker scripts position sections; LTO defers codegen to link.
- `ldd`, `nm -D`, `LD_DEBUG=bindings`.
Verify: binary runs with only the intended libraries.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
