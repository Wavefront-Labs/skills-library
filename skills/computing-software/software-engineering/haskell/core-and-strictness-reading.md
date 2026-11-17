---
id: computing-software.software-engineering.haskell.core-and-strictness-reading
name: core-and-strictness-reading
category: computing-software
field: software-engineering
product: haskell
tags: [haskell, ghc-core, ddump-simpl, strictness-analysis, worker-wrapper, boxed-unboxed, ddump-stg, dsuppress, ghc-prim, levity, core-and-strictness-reading]
level: sme
status: draft
description: "Dump and read GHC Core (-ddump-simpl) to confirm unboxing, worker/wrapper and fusion, using -dsuppress flags and strictness signatures."
sources: ["https://downloads.haskell.org/ghc/latest/docs/users_guide/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Reading Core

**Goal:** verify what the optimiser did instead of guessing.

```bash
ghc -O2 -ddump-simpl -dsuppress-all -dsuppress-uniques -ddump-to-file Foo.hs
# output: Foo.dump-simpl  (next to the object file, or under dist-newstyle with cabal ... --ghc-options)
cabal build --ghc-options="-ddump-simpl -dsuppress-all -ddump-to-file"
```
Other dumps: `-ddump-stg-final` (closer to machine), `-ddump-asm`, `-ddump-cmm`, `-ddump-spec`, `-ddump-rule-firings`, `-ddump-str-signatures`, `-ddump-hi` (interface; `ghc --show-iface Foo.hi`).

## What to look for
- Constructors like `I#` (boxed Int) allocated in a hot loop: missing strictness or unboxing. Worker functions named `$wgo` take unboxed `Int#`.
- `let` bindings with lazy thunks in loops.
- Dictionary arguments (`$dNum`) passed repeatedly: missing specialisation.
- Strictness signature notation in `-ddump-str-signatures`: `<1L>` (strict, used once), `<S>` (strict), `<L>` (lazy). `b` marks diverging results.
- Fusion success: no intermediate list cons cells (`:`) between `map`/`filter`/`sum`.
- `case` on an unboxed tuple `(# s, a #)` is IO/ST state-token code.

## Reading tips
- Core is a small typed lambda calculus; binders are lowercase names, types/coercions are `@`-annotated. `-dsuppress-all` hides them.
- The `ghc-core` tool and the `dump-core` plugin colourise and format (availability varies).
- Compare Core before and after a change using a diff.

## Gotchas
- Core output changes across GHC versions; do not write tooling that parses it casually.
- `-fprof-auto` and `-fhpc` alter Core: dump on the non-profiled build.
- `-O0` Core is unoptimised: always dump with `-O`.
- Heavy reading is rarely needed; first check algorithms and data structures.

## Self-check
- [ ] The hot function's worker uses unboxed arithmetic.
- [ ] Understand each remaining allocation or have a reason to ignore it.
