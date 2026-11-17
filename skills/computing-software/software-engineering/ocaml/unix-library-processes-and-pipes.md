---
id: computing-software.software-engineering.ocaml.unix-library-processes-and-pipes
name: unix-library-processes-and-pipes
category: computing-software
field: software-engineering
product: ocaml
tags: [ocaml, unix-processes, unix-library, create-process, pipe, waitpid, signal]
level: advanced
status: docs-checked
description: "Use the unix library for fork/exec, create_process, pipes, waitpid, signals, select and sockets; know Windows limits."
sources: ["https://ocaml.org/manual/api/", "https://ocaml.org/docs"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Unix library

```ocaml
let run cmd args =
  let pid = Unix.create_process cmd (Array.of_list (cmd :: args)) Unix.stdin Unix.stdout Unix.stderr in
  match Unix.waitpid [] pid with _, Unix.WEXITED c -> c | _ -> -1
let ic = Unix.open_process_in "echo hi"       (* uses sh; shell-injection risk *)
let () = ignore (Unix.close_process_in ic)
let () = Sys.set_signal Sys.sigint (Sys.Signal_handle (fun _ -> exit 130))
```

## Notes
- Prefer `create_process` (argv array, no shell) over `Sys.command`/`open_process_*` with interpolated strings.
- `Unix.fork` fails (raises `Failure`) if any domain has been spawned, and the child may be in a corrupted state if any `Thread` has been spawned.
- Call `Unix.set_close_on_exec` on descriptors you don't want children to inherit; `Unix.pipe ~cloexec:true ()` sets the flag at creation.
- Handle `Unix.Unix_error (e, fn, arg)` with `Unix.error_message e`; `EINTR` means the call was interrupted by a signal.
- Windows supports a subset (no `fork`).

## Self-check
- [ ] Child exit code is propagated; no zombie processes remain.

## Checked

2026-11-03. Confirmed against the OCaml 5.5 manual: the Unix and Sys API pages (create_process, waitpid, process_status WEXITED, open_process_in, close_process_in, pipe ?cloexec, set_close_on_exec, fork behaviour, Unix_error, error_message, stdin/stdout/stderr, Sys.set_signal, Sys.sigint, Signal_handle, Windows limits).

Removed or corrected: real error: `Unix.close_on_exec` does not exist (the function is `Unix.set_close_on_exec`); also the select fd-count claim (only a Windows FD_SETSIZE note is documented) and the Lwt/Eio advice.

Method: documentation only; no commands were run.
