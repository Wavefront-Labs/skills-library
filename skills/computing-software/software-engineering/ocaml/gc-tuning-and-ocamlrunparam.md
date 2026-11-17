---
id: computing-software.software-engineering.ocaml.gc-tuning-and-ocamlrunparam
name: gc-tuning-and-ocamlrunparam
category: computing-software
field: software-engineering
product: ocaml
tags: [ocaml, gc-tuning, ocaml-memory-runtime, ocamlrunparam, gc-set, minor-heap, space-overhead]
level: advanced
status: docs-checked
description: "Tune minor heap size and space_overhead via OCAMLRUNPARAM or Gc.set, read Gc.stat/quick_stat, and use verbose GC logging."
sources: ["https://ocaml.org/manual/", "https://ocaml.org/manual/api/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GC tuning

```bash
OCAMLRUNPARAM='s=4M,o=120,v=0x400' ./main.exe      # minor heap 4M words, space_overhead 120, GC stats at exit
```
```ocaml
let () = Gc.set { (Gc.get ()) with Gc.minor_heap_size = 4_194_304; space_overhead = 120 }
let () = let s = Gc.quick_stat () in Printf.printf "minor=%.0f major=%.0f\n" s.minor_words s.major_words
```

## Notes
- OCamlRunParam letters: `s` minor heap size (words), `o` space_overhead, `b` backtrace, `v` verbosity mask, `l` stack limit, `p` parser trace. Check `ocaml.org/manual/runtime` for the exact set on your version.
- `Gc.Memprof` samples allocated memory words and `Gc.finalise` registers finalisation functions. Always measure before and after tuning.

## Self-check
- [ ] A before/after wall-clock and `Gc.quick_stat` comparison shows the tuning helps.

## Checked

2026-11-03. Confirmed against the OCaml 5.5 manual: the ocamlrun page (OCAMLRUNPARAM letters b, l, o, p, s, v and the v=0x400 statistics bit) and the Gc API page (minor_heap_size, quick_stat, minor_words/major_words, Memprof, finalise).

Removed or corrected: unsourced performance advice (cheap minor allocation, effect of a higher o, compaction latency, OCaml 5 vs 4.14 tuning differences).

Method: documentation only; no commands were run.
