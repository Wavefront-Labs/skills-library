---
id: computing-software.software-engineering.ocaml.exceptions-raise-and-handle
name: exceptions-raise-and-handle
category: computing-software
field: software-engineering
product: ocaml
tags: [ocaml, exceptions, ocaml-errors, exception-definition, try-with, raise-notrace, fun-protect]
level: practitioner
status: docs-checked
description: "Define exceptions, raise/try-with, use raise_notrace, exit codes and cleanup with Fun.protect and the finally pattern."
sources: ["https://ocaml.org/manual/", "https://dev.realworldocaml.org/", "https://github.com/ocaml/ocaml/tree/trunk/stdlib", "https://github.com/ocaml/ocaml/tree/trunk/manual/src"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Exceptions

```ocaml
exception Parse_error of string
let parse s = if s = "" then raise (Parse_error "empty") else s
let r = try Some (parse "") with Parse_error _ -> None
let () = failwith "msg"                  (* raises Failure "msg" *)
let () = invalid_arg "bad"               (* raises Invalid_argument *)
let with_file p f =
  let ic = open_in p in
  Fun.protect ~finally:(fun () -> close_in_noerr ic) (fun () -> f ic)
```

## Notes
- Built-ins: `Not_found`, `Failure`, `Invalid_argument`, `End_of_file`, `Division_by_zero`, `Stack_overflow`, `Out_of_memory`, `Exit`, `Sys_error`.
- Never `try ... with _ -> ...` blindly: it also swallows `Stack_overflow`/`Out_of_memory` and hides bugs. Name the exceptions.
- `Fun.protect ~finally` runs finally even on exceptions; an exception from `finally` becomes `Fun.Finally_raised`.
- `exit n` runs the functions registered with `at_exit`; an uncaught exception aborts the program with exit code 2 (Printexc docs).
- A function that "can fail" should either return `option/result` or document its exception in the `.mli`.

## Self-check
- [ ] No bare `with _ ->` handlers in library code.

## Checked
2026-11-02. Confirmed: predefined exceptions and their declarations, Fun.protect and Finally_raised (fun.mli), at_exit and uncaught-exception exit code 2 (stdlib.mli, printexc.mli). Removed: raise_notrace performance advice and 'flushes std buffers', 'breaks'.
Method: documentation only (OCaml stdlib .mli files and manual .etex sources from github.com/ocaml/ocaml, trunk); no commands were run.
