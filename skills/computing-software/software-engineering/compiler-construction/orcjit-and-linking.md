---
id: computing-software.software-engineering.compiler-construction.orcjit-and-linking
name: orcjit-and-linking
category: computing-software
field: software-engineering
product: compiler-construction
tags: [compiler-construction, orcjit, lli, object-file-emission, compilers, interpreters, language-implementation]
level: practitioner
status: docs-checked
description: "Running generated code"
sources:
  - https://llvm.org/docs/ORCv2.html
  - https://llvm.org/docs/CommandGuide/llc.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ORC JIT and ahead-of-time output

Goal: execute or emit machine code.
- ORC JIT: `LLJIT` uses an `IRCompileLayer` and an `RTDyldObjectLinkingLayer` to compile LLVM IR and link relocatable objects. Compilation is eager on symbol lookup, so a definition is compiled when you look up its address, for example `JIT->lookup("entry")` on an `LLJITBuilder().create()` instance.
- `LLLazyJIT` adds a `CompileOnDemandLayer`: modules added via `addLazyIRModule` compile function bodies on first call.
- Ahead of time: `llc -filetype=obj` emits a native object file (`asm` emits assembly) which is then passed through a native assembler and linker.
- Link runtime support functions (print, gc) from C.
Verify: program output matches interpreter.

## Checked
2026-11-08. Confirmed in the LLVM ORC design and implementation page (LLJIT and LLLazyJIT section) and the llc command guide (`-filetype`, assembler and linker hand-off). Removed: `TargetMachine::addPassesToEmitFile`, the `PassBuilder` optimisation pipeline, and the `lli` tag-only mention, none of which those pages cover.
Method: documentation only; no commands were run.
