---
id: computing-software.software-engineering.haskell.eventlog-threadscope-and-benchmarking
name: eventlog-threadscope-and-benchmarking
category: computing-software
field: software-engineering
product: haskell
tags: [haskell, eventlog, threadscope, criterion, tasty-bench, benchmark, gauge, nf-whnf, hyperfine, rts-l, eventlog-threadscope-and-benchmarking]
level: advanced
status: docs-checked
description: "Record the GHC RTS eventlog (-l, -eventlog) for ThreadScope and ghc-events, and benchmark with criterion or tasty-bench using nf/whnf, env and baselines."
sources: ["https://downloads.haskell.org/ghc/latest/docs/users_guide/runtime_control.html", "https://downloads.haskell.org/ghc/latest/docs/users_guide/phases.html", "https://hackage.haskell.org/package/ghc-events", "https://hackage.haskell.org/package/threadscope", "https://hackage.haskell.org/package/criterion/docs/Criterion-Main.html", "https://hackage.haskell.org/package/tasty-bench/docs/Test-Tasty-Bench.html", "https://hackage.haskell.org/package/base/docs/Debug-Trace.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Eventlog, ThreadScope and benchmarking

**Goal:** see concurrency/GC timelines and measure performance reliably.

## Eventlog
```bash
ghc -O2 -eventlog -rtsopts App.hs
./App +RTS -l -RTS           # writes App.eventlog
threadscope App.eventlog     # graphical viewer of thread profile information
```
User events: `Debug.Trace.traceEvent`, `traceMarker`, `traceEventIO`. `ghc-events show App.eventlog` dumps the log as text. `--eventlog-flush-interval=<seconds>` flushes periodically, for live consumers.

## Benchmarks
```haskell
import Criterion.Main
main = defaultMain
  [ bgroup "fib" [ bench "fib 20" $ whnf fib 20
                 , bench "sort 1e4" $ nf sort input ] ]   -- nf forces the whole result
```
Package `criterion` outputs HTML, CSV and JSON and reports outlier-introduced variance. `tasty-bench` is a one-file framework whose benchmarks are regular Tasty tests, with an API mimicking criterion (`bench "x" $ nf f arg`, `defaultMain`); run with `--csv FILE`, then rerun with `--baseline FILE` to compare.

## Pitfalls
- `whnf` vs `nf`: evaluating only to WHNF measures almost nothing for lists and trees.
- Build large test data outside the timed part with `env` (criterion and tasty-bench both provide it; criterion also has `perRunEnv`); tasty-bench's `env` must not change benchmark names or hierarchy.
- Build optimised (`-O2`).

## Gotchas
- Linking with `-eventlog` is deprecated since GHC 9.4, whose RTS includes eventlog support by default; older GHC needs it.
- Restrict event classes with `-l` flags: `s` scheduler, `g` GC, `p` sparks (sampled), `f` sparks (accurate), `u` user events, `a` all, `-x` disables class x; `-l-ag` leaves only GC events.

## Self-check
- [ ] Benchmarks use `nf` for structure results.
- [ ] Reported variance is small (or the run is repeated).

## Checked
2026-11-03. Confirmed against the GHC users guide (`-eventlog` deprecation, `-l` flags, `--eventlog-flush-interval`), the ghc-events, threadscope, criterion (`Criterion.Main`: `nf`, `whnf`, `env`, `perRunEnv`, `bgroup`, `defaultMain`) and tasty-bench (`--csv`, `--baseline`, `env`) pages, and `Debug.Trace` (`traceEvent`, `traceMarker`, `traceEventIO`). Removed: `-threaded`/`-N4` usage, eventlog-socket, gauge, float-out sharing claim, hyperfine and `+RTS -s` advice, CI threshold advice, per-capability GUI description.
Method: documentation only; no commands were run.
