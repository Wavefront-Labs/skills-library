---
id: computing-software.software-engineering.compiler-construction.register-vms-and-dispatch
name: register-vms-and-dispatch
category: computing-software
field: software-engineering
product: compiler-construction
tags: [compiler-construction, register-based-vm, threaded-code, computed-goto, compilers, interpreters, language-implementation]
level: practitioner
status: draft
description: "Faster interpreters"
sources: ["https://craftinginterpreters.com/", "https://llvm.org/docs/", "https://llvm.org/docs/tutorial/", "https://mlir.llvm.org/docs/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Register VMs and dispatch techniques

Goal: reduce interpreter overhead.
- Register VMs (Lua) use fewer instructions; direct/indirect threaded code and computed goto cut dispatch cost.
- Superinstructions and quickening specialise hot paths.
- Benchmark instruction mix.
Verify: speedup on a loop benchmark with perf counters showing fewer mispredictions.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
