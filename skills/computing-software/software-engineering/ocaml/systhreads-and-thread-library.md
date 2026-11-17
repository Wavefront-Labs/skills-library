---
id: computing-software.software-engineering.ocaml.systhreads-and-thread-library
name: systhreads-and-thread-library
category: computing-software
field: software-engineering
product: ocaml
tags: [ocaml, threads-systhreads, thread-module, threads-posix, master-lock]
level: advanced
status: docs-checked
description: "Use Thread and Event, understand the per-domain domain lock, and when to use threads versus domains."
sources: ["https://ocaml.org/manual/", "https://ocaml.org/manual/api/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Systhreads

```ocaml
let t = Thread.create (fun () -> Thread.delay 0.1; print_endline "done") ()
let () = Thread.join t
```

## Notes
- Within one domain at most one thread executes OCaml code at a time, enforced by a domain lock; a C primitive that blocks can release it. Use `Domain.spawn` for parallel execution.
- Use `Mutex`/`Condition`; `Event` provides synchronous channels (`new_channel`, `send`, `receive`, `sync`).
- After `Unix.fork`, if any thread has been spawned the child process might be in a corrupted state.

## Self-check
- [ ] The program joins all threads before exit.

## Checked

2026-11-03. Confirmed against the OCaml 5.5 manual: the Thread, Event, Mutex and Condition API pages, the C interface chapter (domain lock) and the Unix.fork documentation.

Removed or corrected: the dune library name, the OCaml 4.x global-lock history, the tick-thread preemption claim and the master-lock wording.

Method: documentation only; no commands were run.
