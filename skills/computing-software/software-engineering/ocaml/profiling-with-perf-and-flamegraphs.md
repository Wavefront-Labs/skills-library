---
id: computing-software.software-engineering.ocaml.profiling-with-perf-and-flamegraphs
name: profiling-with-perf-and-flamegraphs
category: computing-software
field: software-engineering
product: ocaml
tags: [ocaml, perf-profiling, ocaml-performance, perf, flamegraph, profiling, call-graph]
level: advanced
status: draft
description: "Profile ocamlopt binaries using Linux perf and flamegraphs, with frame pointers or DWARF call graphs, and interpret OCaml symbols."
sources: ["https://ocaml.org/manual/", "https://ocaml.org/docs"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# perf profiling

```bash
dune build --profile release ./bin/main.exe
perf record --call-graph dwarf -F 999 ./_build/default/bin/main.exe
perf report --no-children
perf script | stackcollapse-perf.pl | flamegraph.pl > out.svg      # Brendan Gregg's FlameGraph scripts
```

## Notes
- OCaml native code can be profiled with `perf`; `--call-graph dwarf` works with `-g` binaries without frame pointers. An opam switch with `ocaml-option-fp` gives frame pointers (OCaml 4.x/5.x variant) for cheaper stacks.
- Names appear as `camlModule__fn_N`; GC work shows as `caml_major_collection_slice`, `caml_oldify*`, `caml_alloc*`.
- Heavy time in GC → check allocation (see memtrace-and-allocation-profiling).
- Use release profile (flambda switch if available) for representative timing; dev may skip optimisation.
- `perf stat` for counters; `hyperfine` for wall-clock comparisons.
- macOS: Instruments or `sample`; Windows: use Visual Studio/Windows Performance Analyzer.

## Self-check
- [ ] Flamegraph attributes time to your hot function, not mostly the GC.
