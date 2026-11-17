---
id: computing-software.software-engineering.ocaml.eio-main-switch-and-fibers
name: eio-main-switch-and-fibers
category: computing-software
field: software-engineering
product: ocaml
tags: [ocaml, eio-basics, ocaml-eio, eio-main-run, eio-switch, eio-fiber, structured-concurrency]
level: advanced
status: docs-checked
description: "Run Eio programs with Eio_main.run, structure concurrency with Switch and Fiber.both/first/fork, and pass capabilities from env."
sources: ["https://github.com/ocaml-multicore/eio", "https://ocaml.org/p/eio"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Eio basics

```ocaml
(* dune: (libraries eio_main) *)
let () =
  Eio_main.run @@ fun env ->
  let clock = Eio.Stdenv.clock env in
  Eio.Fiber.both
    (fun () -> Eio.Time.sleep clock 0.1; Eio.traceln "a")
    (fun () -> Eio.Time.sleep clock 0.1; Eio.traceln "b")
```

## Notes
- Eio uses OCaml 5 effects, so code is direct style without monads. The README states OCaml 5.2.0 or later is needed.
- `Eio_main.run` selects the backend for your platform (`Eio_linux` io_uring, `Eio_posix`, `Eio_windows` which is incomplete). `Eio_mock.Backend.run` can replace it in tests that touch nothing outside.
- `env` carries the capabilities (`Eio.Stdenv.stdout`, `clock`, `net`, `cwd`, `fs`, `domain_mgr`); all authority starts at `Eio_main.run`, so pass a function only what it needs.
- `Eio.Switch.run (fun sw -> ...)` bounds the lifetime of fibers and resources attached to it; it waits for `fn` and all attached fibers, then releases attached resources. `Eio.Fiber.fork ~sw` needs a switch because the new fiber outlives the call; `Fiber.fork_daemon` cancels the fiber when the switch finishes.
- Every fiber has a cancellation context. If one `Fiber.both` fiber fails, the other is cancelled and the original exception is re-raised. Any operation that can switch fibers may raise `Cancelled`.
- `Fiber.first` returns the first fiber to finish and cancels the other. It is not reliable for ensuring exactly one of two actions happens, since both may complete at once.
- `Eio.traceln` is printf-style debugging that needs no stderr plumbing and is safe from multiple domains.

## Self-check
- [ ] The example completes in about 0.1 s, not 0.2 s.

## Checked
Date: 2026-11-08. Confirmed against the Eio README (github.com/ocaml-multicore/eio): effects and OCaml 5.2.0, backends, `Eio_main.run`, `traceln`, `Fiber.both`/`first`, cancellation contexts, `Switch.run`/`fork`/`fork_daemon`, the Stdenv capabilities, `Time.sleep` and `Eio_mock`. Read by searching and reading the relevant README sections, not line by line in full. Removed: the `Fiber.all` mention, the claim about `Eio.Cancel.Cancelled` as a full module path (the README says `Cancelled` exception), and the remark about API churn before 1.0.
Method: documentation only; no commands were run.
