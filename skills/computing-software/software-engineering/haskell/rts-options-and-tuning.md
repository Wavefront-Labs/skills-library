---
id: computing-software.software-engineering.haskell.rts-options-and-tuning
name: rts-options-and-tuning
category: computing-software
field: software-engineering
product: haskell
tags: [haskell, rts, rtsopts, -with-rtsopts, gc-tuning, -a, -n, -h, -k, -xn, nonmoving-gc, compact-regions, heap-size, rts-options-and-tuning]
level: advanced
status: docs-checked
description: "Set RTS flags (-N, -A, -M, -K, -s, -xn) at link or run time with -rtsopts and -with-rtsopts, and tune allocation area, heap limit and GC choices."
sources: ["https://downloads.haskell.org/ghc/latest/docs/users_guide/runtime_control.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# RTS options and GC tuning

**Goal:** control the GHC runtime system's memory and threading behaviour.

## Enabling
```bash
ghc -O2 -threaded -rtsopts "-with-rtsopts=-N -A64m" App.hs
./App +RTS -s -RTS args           # -s: GC and productivity summary
GHCRTS='-N4' ./App                # environment alternative (works only if rtsopts enabled)
```
In a cabal file: `ghc-options: -threaded -rtsopts "-with-rtsopts=-N -A64m"`.

## Common flags
- `-N[x]`: number of capabilities (cores); `-N` uses all cores.
- `-A<size>`: allocation area per capability (default 4MB in recent GHC; larger often speeds allocation-heavy code).
- `-M<size>`: maximum heap; the runtime raises an exception on the main thread when exceeded (after the `-Mgrace` period) instead of swapping; the default is unlimited. `-K<size>`: max stack per thread (default 80% of physical memory; 0 disables the limit).
- `-s`/`-S`: GC statistics; `-h*` heap profiling; `-l` eventlog; `-p` time profile (needs `-prof`).
- `-c<n>`: switch to compacting collection when live data exceeds n% of the `-M` limit (default 30; no effect without `-M`); `-xn` (alias `--nonmoving-gc`, since GHC 8.10.1): non-moving old-generation GC.
- `-I<sec>`: idle time before an idle GC (default 0.3 s in the threaded RTS, 0 in the non-threaded one); `-I0` disables idle GC.
- `-qg`: with no argument, turns parallel GC off (sequential GC); `-qn<n>`: number of GC threads (default min of `-N` and cores).
- `+RTS --info` prints build information of the RTS.

## Reading `-s`
Productivity = mutator time / total; below ~90 percent suggests GC pressure. "max residency" is live data.

## Gotchas
- `-rtsopts[=none|some|all|ignore|ignoreAll]` controls which RTS options the command line may set (and whether `GHCRTS` is read: it is ignored for `none` and `ignoreAll`); permitting all lets users change behaviour, so for untrusted settings use `-rtsopts=none` plus baked-in `-with-rtsopts`.
- `-N` greater than physical cores hurts; in containers `-N` may detect the host's cores; set an explicit count such as `-N4`.
- Large `-A` with many cores multiplies memory (`-A * -N`).

## Self-check
- [ ] `./App +RTS --info` runs, flags documented in README.
- [ ] Changing `-A` has measured benefit.

## Checked

2026-11-02. Confirmed against the GHC User's Guide runtime_control page: -A, -M, -K, -c, -I, -qg, -qn, -xn, -rtsopts, GHCRTS, -s. Removed or fixed: -maxN, wrong -c description, HeapOverflow wording.
Method: documentation only; no commands were run.
