---
id: computing-software.software-engineering.ocaml.microbenchmarks-with-bechamel-core-bench
name: microbenchmarks-with-bechamel-core-bench
category: computing-software
field: software-engineering
product: ocaml
tags: [ocaml, benchmarking, bechamel, core-bench, microbenchmark, opaque-identity]
level: advanced
status: draft
description: "Write stable microbenchmarks with bechamel or Core_bench, avoid dead-code elimination via Sys.opaque_identity, and compare variants."
sources: ["https://ocaml.org/manual/", "https://ocaml.org/docs"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Benchmarking

```ocaml
(* core_bench *)
open Core_bench
let () = Command_unix.run (Bench.make_command [
  Bench.Test.create ~name:"sum" (fun () -> ignore (Sys.opaque_identity (sum_list l))) ])
```

## Notes
- `Sys.opaque_identity` stops the optimiser removing a computation whose result is unused or hoisting constants.
- Use release profile; run on a quiet machine; compare relative numbers, not absolutes.
- bechamel: measures several metrics (time, minor allocations) with linear regression; core_bench reports time, allocations, GC per run.
- Warm up and use enough repetitions; check the confidence intervals the tool prints.
- Alternative: `hyperfine` for end-to-end commands.
- API details differ per library version; follow each library's README.

## Self-check
- [ ] Benchmark result changes when you change the algorithm, not when you add an unrelated print.
