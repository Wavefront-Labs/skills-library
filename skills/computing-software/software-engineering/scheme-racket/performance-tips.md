---
id: computing-software.software-engineering.scheme-racket.performance-tips
name: performance-tips
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, performance-tips]
level: practitioner
status: docs-checked
description: "Speed up code with in-* sequence forms in for, module-level definitions, avoiding set!, fixnum/flonum ops, precompiled regexps and raco make."
sources:
  - https://docs.racket-lang.org/guide/performance.html
  - https://docs.racket-lang.org/guide/for.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Performance tips from the Guide
**Goal:** low-effort wins.
- Prefer `(for ([x (in-list l)]) ...)` over a generic sequence: `in-list`, `in-vector`, `in-range` and similar let `for` generate a fast loop, and a quoted literal list in a clause is treated the same way.
- Time and profile in plain `racket`, not the DrRacket REPL: DrRacket's debugging instrumentation can significantly degrade performance, and the Guide recommends non-interactive module mode.
- Keep code in modules: the compiler can inline `+` and other bindings from `racket/base`, and module-level definitions cannot be mutated when no `set!` is visible, which enables inlining and constant propagation.
- Avoid `set!` on variables in hot code: it can allocate a new location per iteration and hide bindings from the optimizer.
- `raco make` and `raco setup` write compiled bytecode to files so programs are not compiled from source on every run.
- Fixnum arithmetic is never boxed; flonums usually are, so `racket/flonum` operations help the compiler avoid boxing. The `racket/unsafe/ops` functions skip checks and can crash or corrupt memory if misused.
- Compile regexps once (`regexp`, or an `#rx` / `#px` literal) instead of passing a pattern string on every match.
- The default implementation is Racket CS (BC was the default until version 8.0); `(system-type 'vm)` reports `'chez-scheme` for CS and `'racket` for BC.
## Self-check
Time a loop with and without `in-list` using `time`.

## Checked
2026-11-08. Confirmed on the Racket Guide chapter 19 (Performance: sections 19.1 to 19.12) and Guide section 11.10 (Iteration Performance). Removed the unsupported advice to use vectors or hashes instead of `list-ref` / `assoc` and the claim that `racket/base` speeds startup; the `racket/base` statement now follows the Guide's inlining text. Added documented tips on `set!`, DrRacket instrumentation, fixnum / flonum, unsafe ops and regexp compilation.
Method: documentation only; no commands were run.
