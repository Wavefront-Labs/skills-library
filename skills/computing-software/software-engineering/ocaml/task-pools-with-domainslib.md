---
id: computing-software.software-engineering.ocaml.task-pools-with-domainslib
name: task-pools-with-domainslib
category: computing-software
field: software-engineering
product: ocaml
tags: [ocaml, domainslib-tasks, ocaml-parallel-patterns, domainslib, task-pool, parallel-for, data-parallel]
level: advanced
status: docs-checked
description: "Use domainslib Task.setup_pool, run, async/await, parallel_for and parallel_scan for data-parallel work on OCaml 5."
sources: ["https://github.com/ocaml-multicore/domainslib", "https://github.com/ocaml-multicore/domainslib/blob/main/lib/task.mli"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# domainslib

```ocaml
module T = Domainslib.Task
let sum_array a =
  let pool = T.setup_pool ~num_domains:3 () in           (* 3 new domains + the caller = 4 *)
  let r = T.run pool (fun () ->
    T.parallel_for_reduce pool ( + ) 0 ~start:0 ~finish:(Array.length a - 1)
      ~body:(fun i -> a.(i))) in
  T.teardown_pool pool; r
```

## Notes
- `setup_pool ?name ~num_domains ()` creates `num_domains` new domains; `get_num_domains pool` counts the parent too. With `num_domains = 0` the pool is empty and every function runs sequentially in the calling domain. A negative value raises `Invalid_argument`.
- `T.run pool task` encloses calls that await on promises, including `await`, `parallel_for` and variants; outside it those raise `Unhandled`.
- `T.async pool f` returns a promise; `T.await pool p` returns the result or re-raises the task's exception.
- `parallel_for ?chunk_size ~start ~finish ~body pool` runs iterations in any order; the default chunk size is `max(1, (finish-start+1) / (8 * num_domains))`. `parallel_for_reduce` takes `pool reduce init`; reductions happen in arbitrary order, so the reduce function must be associative for a deterministic result.
- `parallel_scan pool op array` returns an array of reduced intermediate values (also needs an associative `op`). `parallel_find` stops once a body returns `Some v`.
- The README example parallelises Fibonacci with `async`/`await` and switches to sequential code below a size threshold (`n > 20`) so tasks stay large enough.
- Install with opam (`opam install domainslib`); the README example uses an OCaml 5.3.0 switch.

## Self-check
- [ ] The parallel sum equals the sequential sum.

## Checked
Date: 2026-11-08. Confirmed against the domainslib README and `lib/task.mli` on GitHub (pool setup, run, async/await, parallel_for, parallel_for_reduce, parallel_scan, parallel_find, defaults). Removed: the `Domain.recommended_domain_count () - 1` advice, the Atomic/Mutex shared-data advice, the speed-up self-check and the version caveat.
Method: documentation only; no commands were run.
