---
id: computing-software.software-engineering.ocaml.stdlib-misc-sys-random-atomic
name: stdlib-misc-sys-random-atomic
category: computing-software
field: software-engineering
product: ocaml
tags: [ocaml, seq-gc-misc-stdlib, sys-module, random-module, filename-module, sys-getenv]
level: practitioner
status: docs-checked
description: "Use Sys.argv, Sys.getenv_opt, Filename, Random (self_init, State) and Gc stat helpers from Stdlib."
sources: ["https://ocaml.org/manual/api/", "https://ocaml.org/docs"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sys, Filename, Random, Gc

```ocaml
let args = Array.to_list Sys.argv           (* argv.(0) is the program *)
let home = Sys.getenv_opt "HOME"
let () = if Sys.file_exists "x" then Sys.remove "x"
let p = Filename.concat "dir" "f.txt"       Filename.extension p   Filename.basename p
let () = Random.self_init ()                 (* otherwise the same sequence each run *)
let n = Random.int 100                      (* bound < 2^30 *)
let s = Random.State.make [| 42 |]          (* reproducible, independent state *)
let st = Gc.quick_stat ()
```

## Notes
- `Sys.getenv` raises `Not_found`; `Sys.command` runs a shell command (injection risk; use `Unix.create_process`).
- `Random` is a pseudo-random number generator; use a dedicated cryptographic library for secrets.
- The basic `Random` functions use a domain-local generator, shared by all threads of one domain.
- `Sys.os_type` (`"Unix"`, `"Win32"`, `"Cygwin"`), `Sys.word_size`, `Sys.time` (CPU time), `Unix.gettimeofday` for wall clock.

## Self-check
- [ ] Reproducible tests use `Random.State.make`, not the global state.

## Checked

2026-11-03. Confirmed against the OCaml 5.5 manual: the Sys, Filename, Random and Gc API pages (getenv_opt, remove, file_exists, command, os_type values, Random.int bound below 2^30, self_init, domain-local generator, Filename.concat/extension/basename, Gc.quick_stat, Unix.gettimeofday).

Removed or corrected: third-party RNG advice (mirage-crypto-rng, /dev/urandom) and the OCaml 4 versus 5 seed-sequence comparison.

Method: documentation only; no commands were run.
