---
id: computing-software.software-engineering.cpp.perf-flamegraphs-valgrind-and-assembly-inspection
name: perf-flamegraphs-valgrind-and-assembly-inspection
category: computing-software
field: software-engineering
product: cpp
tags: [cpp, cpp-profiling, cpp-pr-perf, cpp-pr-valgrind, cpp-pr-asm, perf, flamegraph, callgrind, massif, compiler-explorer, perf-flamegraphs, callgrind-massif, compiler-explorer-assembly]
level: practitioner
status: draft
description: "Profile C++ with perf and flame graphs, callgrind and massif, and inspect generated assembly with objdump or Compiler Explorer to confirm optimisations."
sources: ["https://perf.wiki.kernel.org/index.php/Tutorial", "https://valgrind.org/docs/manual/cl-manual.html", "https://godbolt.org/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# perf, flame graphs, Valgrind and assembly inspection

## Build for profiling
Optimised with symbols and frame pointers: `g++ -O2 -g -fno-omit-frame-pointer`. Do not profile `-O0`.

## perf (Linux)
```
perf stat -d ./app                              # cycles, IPC, branch and cache misses overview
perf record -F 999 --call-graph dwarf ./app     # or --call-graph fp (cheaper) / lbr
perf report --no-children                       # TUI: where self time goes
perf annotate -s symbol                         # per-instruction hot spots
perf script | stackcollapse-perf.pl | flamegraph.pl > flame.svg      # Brendan Gregg's FlameGraph scripts
```
Wide flame-graph boxes are expensive stacks. Alternative viewers: Hotspot, Firefox Profiler (`perf script -F +pid > out.perf`), speedscope. `perf` may need `sysctl kernel.perf_event_paranoid=1` in containers.

## Valgrind tools (slow: 20-50x, deterministic)
```
valgrind --tool=callgrind --dump-instr=yes ./app && kcachegrind callgrind.out.*       # call counts and inclusive cost
valgrind --tool=massif --time-unit=B ./app && ms_print massif.out.*                    # heap usage over time
valgrind --tool=cachegrind --branch-sim=yes ./app
```
Use on small, representative inputs; `--toggle-collect=ns::function` restricts to one function. Not available natively on Windows; macOS support lags.

## Inspect assembly
```
g++ -O2 -S -fverbose-asm -masm=intel f.cpp -o -  | c++filt
objdump -d -C --no-show-raw-insn -M intel app | less
```
Compiler Explorer (godbolt.org) shows source-to-asm mapping for many compilers; add `-O2 -march=native -std=c++20`, use `-fopt-info-vec` (GCC) or `-Rpass=loop-vectorize` (Clang) to see vectorisation decisions. Check that the hot loop is inlined, vectorised and free of calls you did not expect.

## Gotchas
- Sampling profilers bias to code with symbols; inlined frames need `-g`.
- Run on an idle, frequency-stable machine; compare against a baseline binary with the same flags.
- Compiler Explorer builds differ from your toolchain (flags, headers); confirm on the real binary.
- Profiling the wrong build type (assert-heavy debug) misleads.

## Verify
- [ ] Flame graph points at the same top function across three runs.
- [ ] After an optimisation, `perf stat` shows fewer cycles for identical output and tests still pass.
