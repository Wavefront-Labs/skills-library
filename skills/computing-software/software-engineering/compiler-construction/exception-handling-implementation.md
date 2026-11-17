---
id: computing-software.software-engineering.compiler-construction.exception-handling-implementation
name: exception-handling-implementation
category: computing-software
field: software-engineering
product: compiler-construction
tags: [compiler-construction, zero-cost-exceptions, landing-pads, setjmp-longjmp, compilers, interpreters, language-implementation]
level: practitioner
status: draft
description: "Unwinding"
sources: ["https://craftinginterpreters.com/", "https://llvm.org/docs/", "https://llvm.org/docs/tutorial/", "https://mlir.llvm.org/docs/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Exception handling implementation

Goal: implement exceptions.
- Zero-cost model: tables map PC ranges to landing pads; unwinder walks frames using CFI (Itanium ABI, `_Unwind_RaiseException`). Alternatives: setjmp/longjmp, return-code propagation, result types.
- Cleanup (`finally`) and destructors run on unwind.
- Cost is paid when throwing.
Verify: throw/catch works across frames with cleanups run.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
