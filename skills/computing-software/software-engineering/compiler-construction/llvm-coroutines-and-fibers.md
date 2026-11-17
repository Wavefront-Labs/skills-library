---
id: computing-software.software-engineering.compiler-construction.llvm-coroutines-and-fibers
name: llvm-coroutines-and-fibers
category: computing-software
field: software-engineering
product: compiler-construction
tags: [compiler-construction, llvm-coro, stackful-coroutine, context-switch-asm, compilers, interpreters, language-implementation]
level: practitioner
status: docs-checked
description: "Runtime support"
sources:
  - https://llvm.org/docs/Coroutines.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# LLVM coroutines

Goal: use backend support.
- LLVM coroutines are functions with one or more `llvm.coro.suspend` intrinsics; a suspended coroutine can be resumed or destroyed.
- Standard switched-resume lowering (`llvm.coro.id`) splits a coroutine into a ramp function, resume and destroy parts; the frontend calls the ramp function, which returns the coroutine object, and always resumes or destroys through `llvm.coro.resume` and `llvm.coro.destroy`. Destroy is required even after normal completion.
- Returned-continuation lowering (`llvm.coro.id.retcon`, `llvm.coro.id.retcon.once`) returns a continuation function pointer plus yielded values at each suspend; async lowering uses `llvm.coro.id.async`.
- A coroutine frame is built with `llvm.coro.id`, `llvm.coro.begin`, `llvm.coro.free` and `llvm.coro.end`.
Verify: a resume/destroy test runs through the switched-resume ABI.

## Checked
2026-11-08. Confirmed in the LLVM Coroutines page (Switched-Resume, Returned-Continuation and Async-Continuation lowering sections, plus the examples). Removed: stackful fibres, hand-written context switches, guard pages, and the 100k-coroutine memory test, none of which the page covers.
Method: documentation only; no commands were run.
