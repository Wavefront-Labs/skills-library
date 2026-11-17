---
id: computing-software.software-engineering.ocaml.lwt-parallel-composition
name: lwt-parallel-composition
category: computing-software
field: software-engineering
product: ocaml
tags: [ocaml, lwt-concurrency, lwt-join, lwt-list-iter-p, lwt-pool, lwt-mutex]
level: practitioner
status: docs-checked
description: "Run promises concurrently with Lwt.both/join/all, Lwt_list _p vs _s, Lwt_pool and Lwt_mutex; race with Lwt.pick."
sources: ["https://raw.githubusercontent.com/ocsigen/lwt/master/src/core/lwt.mli", "https://raw.githubusercontent.com/ocsigen/lwt/master/src/core/lwt_list.mli", "https://raw.githubusercontent.com/ocsigen/lwt/master/src/core/lwt_mutex.mli", "https://raw.githubusercontent.com/ocsigen/lwt/master/src/core/lwt_pool.mli"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Lwt concurrency

```ocaml
open Lwt.Syntax
let both = Lwt.both (fetch 1) (fetch 2)          (* both promises already started *)
let all  = Lwt_list.map_p fetch [1;2;3]          (* _p: parallelised; map_s: sequential *)
let m = Lwt_mutex.create ()
let guarded f = Lwt_mutex.with_lock m f
let pool = Lwt_pool.create 10 (fun () -> make_conn ())
let query q = Lwt_pool.use pool (fun c -> run c q)
```

## Notes
- `Lwt.both p1 p2` is pending until both resolve, then gives the pair. If either is rejected, the result is rejected with one such exception (chosen arbitrarily), but only after both have resolved. `and*` / `and+` in `Lwt.Syntax` are syntax for `both`.
- `Lwt.join : unit t list -> unit t` waits for all, with the same rejection rule. `Lwt.all : 'a t list -> 'a list t` (since 5.1.0) also returns the values; if any promise is rejected none of the values are available.
- `Lwt.pick ps` resolves when one promise resolves and tries to cancel the others; `Lwt.choose` does not cancel. An empty list raises `Invalid_argument`. The Lwt docs discourage cancellation in new code.
- `Lwt_list` has `iter`, `map`, `mapi`, `rev_map`, `for_all`, `exists` and others in `_s` (sequential) and `_p` (parallelised) forms; `fold_left_s` and `fold_right_s` exist only sequentially.
- `Lwt_mutex.with_lock m f` calls `f ()` with the mutex locked and unlocks it even if `f` raises. Waiters are woken in the order they tried to lock.
- `Lwt_pool.create n ?validate ?check ?dispose f` makes a pool of at most `n` elements, created on demand and reused. `use p f` gives an element to `f`, returns it afterwards, and waits when all `n` are in use. `clear p` disposes elements. It does not pool system threads; for that use `Lwt_preemptive`.

## Self-check
- [ ] Three 1-second sleeps in `Lwt.join` finish in about 1 second.

## Checked
Date: 2026-11-08. Confirmed against lwt.mli (both, join, all, pick, choose, Syntax), lwt_list.mli (signatures), lwt_mutex.mli and lwt_pool.mli on GitHub, read in full for mutex and pool; lwt.mli read for the concurrency, Syntax and cancellation sections only. Removed: the ocsigen.org and ocaml.org/docs sources (unreadable stubs), the claim that `_p` has no cap, the claim that Lwt is single-domain, the lwt_eio coexistence note and the sequential-versus-concurrent code advice.
Method: documentation only; no commands were run.
