---
id: computing-software.software-engineering.haskell.ghc-optimisation-levels-and-flags
name: ghc-optimisation-levels-and-flags
category: computing-software
field: software-engineering
product: haskell
tags: [haskell, ghc-o2, optimisation-flags, -fllvm, -fspecialise, -fexpose-all-unfoldings, -funbox-strict-fields, lto, -j, ghc-optimisation-levels-and-flags, haskell-optimisation]
level: practitioner
status: docs-checked
description: "Choose -O0/-O1/-O2, useful flags (-fspecialise-aggressively, -funbox-strict-fields, -fexpose-all-unfoldings, -j), and cabal ghc-options placement."
sources: ["https://downloads.haskell.org/ghc/latest/docs/users_guide/using-optimisation.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GHC optimisation levels

**Goal:** get good performance from release builds, fast builds in development.

## Levels
- `-O0`: no optimisation (what plain `ghc` does when no `-O` option is given; cabal's default level is documented in the Cabal user guide, confirm there). Fast compile, slow code. Use `-O0` in dev (`cabal build --ghc-options=-O0` or `optimization: False` in cabal.project).
- `-O` / `-O1`: standard optimisations. `-O2`: applies every non-dangerous optimisation, including `-fspec-constr` and `-fliberate-case`; significantly longer compile times, often small gains. Any `-On` with n > 2 equals `-O2`.
- `-fllvm`: LLVM back end (needs LLVM tools installed, confirm the supported LLVM version in the User's Guide; benefits numeric loops sometimes; evaluate before adopting). Native code generator is the default.

## Frequently used flags
- `-funbox-strict-fields` (off by default) and `-funbox-small-strict-fields` (on with `-O`; pointer-sized or smaller fields only): unpack strict fields.
- `-fspecialise-aggressively` and `-fexpose-all-unfoldings`: allow cross-module specialisation of imported overloaded functions (not part of any `-O` level; can massively increase code size).
- `-fworker-wrapper`, `-fstrictness`, `-ffull-laziness`, `-fcse` are on with `-O`; `-fno-full-laziness` and `-fno-cse` rescue code where sharing causes leaks.
- `-flate-dmd-anal`, `-fstatic-argument-transformation` are niche and off by default.
- `-j[N]` parallel module compilation (N defaults to the number of processors); `-with-rtsopts` for runtime.
- `-dynamic`/`-static`/`-threaded`/`-rtsopts`: linking and RTS flavours.

## In the cabal file
```cabal
ghc-options: -O2 -funbox-strict-fields
```
Prefer `cabal.project` for per-developer flags (`package *` `ghc-options`), to avoid forcing consumers of your library to compile with your flags.

## Gotchas
- Measure first: use a benchmark and `+RTS -s`. Most programs gain more from algorithm and data structure choice than flags.
- `-O2` vs `-O1` differences are workload-dependent; do not assume.
- Orphan INLINE changes can cause code bloat; check binary size.
- Changing flags rebuilds everything; flags are part of the build hash.
- `-Wall -Werror` interacts with new GHC releases; use `-Werror` only in CI.

## Self-check
- [ ] Production build uses a documented optimisation level.
- [ ] Dev loop uses `-O0`.

## Checked

2026-11-02. Confirmed against the GHC User's Guide using-optimisation and using pages: -O levels, unboxing flags, specialisation flags, -j. Removed or fixed: wrong unbox default, cabal default level claim.
Method: documentation only; no commands were run.
