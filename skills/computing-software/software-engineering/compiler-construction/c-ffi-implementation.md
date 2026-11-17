---
id: computing-software.software-engineering.compiler-construction.c-ffi-implementation
name: c-ffi-implementation
category: computing-software
field: software-engineering
product: compiler-construction
tags: [compiler-construction, libffi, calling-c-from-vm, struct-marshalling, ffi, c-abi-interop, language-bindings, compilers, interpreters, language-implementation]
level: practitioner
status: draft
description: "Native interop"
sources: ["https://craftinginterpreters.com/", "https://llvm.org/docs/", "https://llvm.org/docs/tutorial/", "https://mlir.llvm.org/docs/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Implementing a C FFI

Goal: call C from your language.
- `dlopen/dlsym` plus libffi (`ffi_prep_cif`, `ffi_call`) to call arbitrary signatures; marshal strings and structs; pin GC objects while native code holds them.
- Callbacks from C need trampolines.
- Validate signatures to avoid crashes.
Verify: calling `strlen` and a struct-returning function works.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
