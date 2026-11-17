---
id: computing-software.software-engineering.ocaml.atomics-mutexes-and-memory-model
name: atomics-mutexes-and-memory-model
category: computing-software
field: software-engineering
product: ocaml
tags: [ocaml, atomic-mutex-memory-model, atomic-module, mutex-protect, condition-variable, memory-model]
level: advanced
status: gated
description: "Protect shared state with Atomic and Mutex/Condition/Semaphore, and know the OCaml 5 data-race-free memory model guarantees."
sources: ["https://ocaml.org/manual/", "https://ocaml.org/manual/api/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Atomics, mutexes, memory model

```ocaml
let counter = Atomic.make 0
let () = Atomic.incr counter                  (* Atomic.fetch_and_add counter 1 *)
let m = Mutex.create ()
let with_lock f = Mutex.protect m f           (* Mutex.protect: OCaml 5.1+ *)
let c = Condition.create ()
let wait_ready ready =
  Mutex.lock m;
  while not !ready do Condition.wait c m done;
  Mutex.unlock m
```

## Notes
- Data-race-free programs behave sequentially consistent. Racy programs have bounded, local-in-time behaviour: they cannot crash the runtime (no out-of-thin-air values), but results are unspecified.
- Plain `ref`, `Hashtbl`, `Queue`, `Buffer` are not thread-safe. Wrap them or use `Atomic`.
- `Atomic.compare_and_set` compares physically (`==`): ok for ints and constant constructors; for boxed values keep the exact old value.
- Always unlock on all paths: `Mutex.protect` or `Fun.protect ~finally:(fun () -> Mutex.unlock m)`.
- Deadlock: acquire multiple mutexes in a consistent order. Re-locking a held mutex raises `Sys_error` (unconfirmed on all platforms).

## Self-check
- [ ] A TSan build (opam switch with `ocaml-option-tsan`, OCaml 5.2+) reports no races.

## Checked

- Date: 2026-11-02.
- Source pages listed in `sources` were fetched where possible; the manual root and API index were fetched but not the Atomic/Mutex/Condition module pages or the memory-model chapter. Treat the specific names, flags and figures as unconfirmed (gated: unconfirmed, source is paywalled or blocked).

Method: documentation only; no commands were run.
