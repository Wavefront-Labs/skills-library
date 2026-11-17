---
id: computing-software.software-engineering.ocaml.lock-free-structures-with-saturn
name: lock-free-structures-with-saturn
category: computing-software
field: software-engineering
product: ocaml
tags: [ocaml, lockfree-saturn, saturn, lock-free, concurrent-queue, work-stealing]
level: advanced
status: docs-checked
description: "Use Saturn lock-free structures (Queue, Stack, Work_stealing_deque) across OCaml 5 domains and respect domain roles."
sources: ["https://github.com/ocaml-multicore/saturn", "https://ocaml-multicore.github.io/saturn/saturn/Saturn/Queue/index.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Saturn

```ocaml
let q : int Saturn.Queue.t = Saturn.Queue.create ()
let () = Saturn.Queue.push q 1
let r = Saturn.Queue.pop_opt q     (* Some 1 *)
```

## Notes
- Saturn is a collection of concurrent-safe data structures for OCaml 5; it needs OCaml 5.2.0 or later (versions of OCaml 5 before 5.2 are unsupported due to bugs in `Atomic`).
- Provided modules: `Stack` (Treiber), `Bounded_stack`, `Queue` (Michael-Scott, MPMC), `Bounded_queue`, `Work_stealing_deque` (Chase-Lev, single producer / multi consumer), `Single_prod_single_cons_queue`, `Single_consumer_queue`, `Skiplist`, `Htbl`, `Bag`.
- `Queue` API: `create`, `of_list`, `is_empty`, `push` (producer), and consumer functions `pop_opt`, `pop_exn` (raises `Empty`), `peek_opt`, `peek_exn`, `drop_exn`.
- Bounded variants add capacity and `length` at a general overhead cost; use the unbounded ones if neither is needed.
- Some structures have domain roles: a single-consumer queue must have only one domain popping at a time, and most `Work_stealing_deque` functions cannot be used by all domains. Breaking roles can compromise safety.
- Saturn structures are not composable: combining operations does not preserve linearizability or lock-freedom.
- `Single_cons_single_prod_unsafe`, `Queue_unsafe`, `Bounded_queue_unsafe` and `Htbl_unsafe` use `Obj.magic` and may be unsafe with `flambda2`; prefer the normal versions.
- Testing uses unit and qcheck tests, STM tests (multicoretests), `dscheck` for non-blocking properties and tsan for data races.

## Self-check
- [ ] Producers on several domains and one consumer see every element exactly once.

## Checked
Date: 2026-11-08. Confirmed against the Saturn README and the Saturn `Queue` API page. Removed: the old name `lockfree`, the "Mutex + Queue is fast enough" advice, `Domain.cpu_relax` spin-wait advice (only seen in an example), and the claim that lock-free implies contention-sensitive throughput.
Method: documentation only; no commands were run.
