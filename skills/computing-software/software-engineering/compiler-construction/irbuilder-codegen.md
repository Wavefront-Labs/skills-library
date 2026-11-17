---
id: computing-software.software-engineering.compiler-construction.irbuilder-codegen
name: irbuilder-codegen
category: computing-software
field: software-engineering
product: compiler-construction
tags: [compiler-construction, irbuilder, llvm-module-context, codegen-visitor, kaleidoscope, llvm-irbuilder, llvm-c-api, compilers, interpreters, language-implementation]
level: practitioner
status: docs-checked
description: "Frontend codegen"
sources:
  - https://llvm.org/docs/tutorial/MyFirstLanguageFrontend/LangImpl03.html
  - https://llvm.org/docs/tutorial/MyFirstLanguageFrontend/LangImpl07.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Generating IR with IRBuilder

Goal: lower an AST to LLVM IR.
- Keep an `LLVMContext`, a `Module` (owns all generated IR, holds functions and globals, has a symbol table) and an `IRBuilder<>` (tracks the insertion point and creates instructions, for example `CreateFAdd`).
- Create functions with `Function::Create(FT, Function::ExternalLinkage, Name, TheModule.get())`; look up callees with `TheModule->getFunction(Callee)`.
- For mutable variables, map names to `AllocaInst*` and create the allocas in the function's entry block; the `mem2reg` pass (`opt -passes=mem2reg`) then promotes them to SSA registers and inserts phi nodes.
- `mem2reg` only promotes entry-block allocas of first-class values with direct loads and stores and array size 1; the `sroa` pass also handles structs and arrays.
- Call `verifyFunction` after emitting a function.
Verify: the module verifies.

## Checked
2026-11-08. Confirmed in the LLVM Kaleidoscope tutorial chapters 3 (code generation) and 7 (mutable variables). Removed: explicit `br`/`phi` construction for if and loops, `verifyModule`, the C API tag claim and the `lli` run step (not covered by the pages read).
Method: documentation only; no commands were run.
