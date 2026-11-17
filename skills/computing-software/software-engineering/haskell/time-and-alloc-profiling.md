---
id: computing-software.software-engineering.haskell.time-and-alloc-profiling
name: time-and-alloc-profiling
category: computing-software
field: software-engineering
product: haskell
tags: [haskell, profiling, prof, cost-centre, fprof-auto, prof-file, hs-prof, ticky, ghc-prof, flamegraph, profiteur, time-and-alloc-profiling, haskell-profiling]
level: advanced
status: draft
description: "Profile with -prof and cost centres (-fprof-auto, SCC), read the .prof file, cabal --enable-profiling, and view flame graphs with profiteur or ghc-prof-flamegraph."
sources: ["https://downloads.haskell.org/ghc/latest/docs/users_guide/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Time and allocation profiling

**Goal:** find where time and allocation go.

```bash
ghc -O2 -prof -fprof-auto-exported -rtsopts App.hs
./App +RTS -p -RTS args         # writes App.prof (-pj for JSON)
cabal run --enable-profiling --profiling-detail=late -- args +RTS -p   # cabal; profiling libs must be installed
```
`cabal build --enable-profiling` rebuilds all dependencies with profiling (need profiling libs: GHC from ghcup includes them for boot libraries; Hackage deps are rebuilt automatically).

## Reading App.prof
Columns: COST CENTRE, MODULE, `%time`, `%alloc` (individual) and inherited. The top lines of the "individual" table are hot spots. The call tree shows entries and who calls whom.

## Choosing cost centres
- `-fprof-auto`: all bindings (distorts optimisation heavily); `-fprof-auto-top`: top-level; `-fprof-auto-exported`; `-fprof-late` (GHC 9.4 and later): add cost centres after optimisation, much less distortion (check availability for your version).
- Manual: `{-# SCC "name" #-}` around an expression; `-fno-prof-count-entries`.
- Recommended order: late/top-level detail first, then add manual SCCs where needed.

## Viewing
```bash
ghc-prof-flamegraph App.prof          # package ghc-prof-flamegraph + flamegraph.pl
profiteur App.prof                    # HTML treemap
```
`hp2ps` for heap profiles (see space-leak skill). `ticky-ticky` profiling (`-ticky`) gives low-overhead counters.

## Gotchas
- Profiled binaries are slower and allocate differently; verify the speedup on an unprofiled `-O2` build.
- Profiling libraries must match the compiler; missing `.p_hi` means a library was not built with profiling.
- Cost centres on small functions prevent inlining, shifting the cost.
- Use `criterion`/`tasty-bench` microbenchmarks to confirm improvement.

## Self-check
- [ ] The hot function is identified by %time and %alloc.
- [ ] After the change, runtime improved in a non-profiled benchmark.
