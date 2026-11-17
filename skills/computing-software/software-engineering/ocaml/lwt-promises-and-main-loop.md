---
id: computing-software.software-engineering.ocaml.lwt-promises-and-main-loop
name: lwt-promises-and-main-loop
category: computing-software
field: software-engineering
product: ocaml
tags: [ocaml, lwt-basics, ocaml-lwt, lwt-bind, lwt-main-run, lwt-promise]
level: practitioner
status: docs-checked
description: "Create and chain Lwt promises with let* / Lwt.bind, run them with Lwt_main.run, and handle stray promises with Lwt.async."
sources: ["https://raw.githubusercontent.com/ocsigen/lwt/master/src/core/lwt.mli", "https://raw.githubusercontent.com/ocsigen/lwt/master/src/unix/lwt_main.mli", "https://raw.githubusercontent.com/ocsigen/lwt/master/src/unix/lwt_preemptive.mli"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Lwt basics

```ocaml
(* dune: (libraries lwt lwt.unix) *)
open Lwt.Syntax
let fetch n = let* () = Lwt_unix.sleep 0.1 in Lwt.return (n * 2)
let main =
  let* a = fetch 1 in
  let* b = fetch 2 in
  let* () = Lwt_io.printlf "%d" (a + b) in
  Lwt.return_unit
let () = Lwt_main.run main
```

## Notes
- `'a Lwt.t` is a promise. Core operations: `Lwt.return`, `Lwt.fail`, `Lwt.bind`, `Lwt.map`, `Lwt.catch`.
- `Lwt.Syntax` provides `let*` (bind), `let+` (map), and `and*` / `and+` (both). The `let%lwt` form needs the `lwt_ppx` package.
- `Lwt_main.run p` runs the scheduler until `p` resolves, returns its value, or raises its exception. Every native or bytecode Lwt program should call it at top level. It is not available when targeting JavaScript.
- Nested `Lwt_main.run` raises `Failure`. Do not call it from a callback of a promise resolved by an outer `Lwt_main.run`.
- Do not call `Lwt_main.run` in a function registered with `Stdlib.at_exit`; use `Lwt_main.at_exit` instead.
- On Unix `Lwt_main.run` installs a `SIGCHLD` handler, so non-Lwt system calls in the same program must handle `EINTR`.
- A top-level promise that is not passed to `bind`, `catch`, `join` etc. and is not the one given to `Lwt_main.run` should be wrapped in `Lwt.async`. Plain `ignore` loses its rejection.
- `Lwt.async f` sends a rejection of `f ()` (or an exception raised by `f ()`) to `Lwt.async_exception_hook`. The default prints the exception and exits non-zero. Applications may reassign the hook; libraries should leave it alone. `Lwt.dont_wait` takes an explicit handler instead.
- `Lwt_preemptive.detach f x` runs `f x` in a preemptive thread and returns a promise. By default the pool is capped at four threads (raise with `Lwt_preemptive.init` or `set_bounds`). Lwt functions generally cannot be used inside `f`; use `Lwt_preemptive.run_in_main` for that.
- `Lwt.pause ()` replaces the deprecated `Lwt_main.yield`.

## Self-check
- [ ] The program exits after `Lwt_main.run` returns and no stray promise is silently dropped.

## Checked
Date: 2026-11-08. Confirmed against lwt.mli, lwt_main.mli and lwt_preemptive.mli on GitHub (read in full for lwt_main and lwt_preemptive's detach section; lwt.mli read for the Syntax module, async, async_exception_hook, concurrency and cancellation sections only). Removed: the ocsigen.org and ocaml.org/docs sources (unreadable stubs), the claim about which Lwt version added Syntax, the claim that blocking calls stall all promises as a rule, the Lwt_unix/Lwt_io function list, and cancellation advice.
Method: documentation only; no commands were run.
