---
id: computing-software.software-engineering.ocaml.eio-files-networking-and-domains
name: eio-files-networking-and-domains
category: computing-software
field: software-engineering
product: ocaml
tags: [ocaml, eio-io-net, eio-path, eio-net, eio-domain-manager, eio-flow]
level: advanced
status: docs-checked
description: "Do file and network I/O with Eio.Path, Eio.Net and Buf_read, and run CPU work in parallel with Eio.Domain_manager.run."
sources: ["https://github.com/ocaml-multicore/eio", "https://ocaml.org/p/eio"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Eio I/O and parallelism

```ocaml
let () = Eio_main.run @@ fun env ->
  let cwd = Eio.Stdenv.cwd env in
  Eio.Path.save ~create:(`Or_truncate 0o644) Eio.Path.(cwd / "out.txt") "hello";
  let s = Eio.Path.load Eio.Path.(cwd / "out.txt") in
  Eio.traceln "%s" s;
  let dm = Eio.Stdenv.domain_mgr env in
  let r = Eio.Domain_manager.run dm (fun () -> heavy_compute 40) in
  Eio.traceln "%d" r
```

## Notes
- An `'a Path.t` is a capability to a base directory plus a relative string path; append with `/`. `env` gives two initial paths: `cwd` (only files beneath the current working directory; escapes via `..`, absolute paths or symlinks out fail with `Permission_denied`) and `fs` (full access like the stdlib).
- `Eio.Path.with_subtree` / `open_subtree` makes a restricted capability for a subdirectory.
- `Path.save` and `Path.load` write and read a whole file; `Path.open_in` / `with_open_in` give a flow and `Path.with_lines` streams lines.
- Network: `Eio.Net.listen net ~sw ~reuse_addr ~backlog addr`, `Eio.Net.run_server socket handler` (accepts and handles clients concurrently), `Eio.Net.with_tcp_connect net ~host ~service`.
- Reading: `Eio.Buf_read.of_flow ~initial_size ~max_size` plus `line`, `take`, `take_all`, `parse`.
- `Eio.Domain_manager.run dm fn` runs `fn` in another domain, waits, and lets other fibers run meanwhile. The function must not touch non-threadsafe values, and the type system does not check this.
- `Eio.Executor_pool` (domain workers with a `~weight` per job) is described as the recommended way to use OCaml 5 multicore.
- Backends: `Eio_linux` (io_uring), `Eio_posix`, `Eio_windows` (incomplete); `Eio_main.run` picks one.

## Self-check
- [ ] The file is written and read back in the same run.

## Checked
Date: 2026-11-08. Confirmed against the Eio README (github.com/ocaml-multicore/eio): the filesystem section (cwd vs fs, Path.save/load/with_lines, subtree checks), networking (run_server, listen, with_tcp_connect), Buf_read, Domain_manager and Executor_pool notes, and the backend list. Read by searching and reading the relevant README sections, not line by line in full. Removed: the claim that `Eio.Flow` is the name used for reads in this skill (kept Buf_read), the "signatures change between releases" remark, and the Atomic/Mutex advice (not stated there).
Method: documentation only; no commands were run.
