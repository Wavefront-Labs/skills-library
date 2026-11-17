---
id: computing-software.software-engineering.scheme-racket.sicp-register-machines
name: sicp-register-machines
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, sicp-register-machines]
level: advanced
status: draft
description: "Simulate register machines with assembler, instruction lists and explicit-control evaluator, and study the SICP compiler (SICP 5.1-5.5)."
sources:
  - https://sarabander.github.io/sicp/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Register machines and compilation
**Goal:** low-level evaluation model.
- Machine: registers, stack, controller instruction sequence (`assign`, `test`, `branch`, `goto`, `save`, `restore`, `perform`).
- Build the simulator first (make-machine, assemble) then GCD and factorial machines.
- The explicit-control evaluator turns the metacircular evaluator into register code; the compiler emits similar code with register usage analysis.
## Self-check
Run the GCD machine on 206 and 40 and get 2.
