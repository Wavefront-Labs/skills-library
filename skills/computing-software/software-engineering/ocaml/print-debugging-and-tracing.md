---
id: computing-software.software-engineering.ocaml.print-debugging-and-tracing
name: print-debugging-and-tracing
category: computing-software
field: software-engineering
product: ocaml
tags: [ocaml, printf-trace-debug, assert-expression, eprintf-debug, trace-directive]
level: intro
status: draft
description: "Use Printf.eprintf, assert, Format-based pp, and the toplevel #trace plus runtime backtrace flags to find bugs fast."
sources: ["https://ocaml.org/manual/", "https://ocaml.org/docs"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Print debugging and tracing

```ocaml
let () = Printf.eprintf "x=%d\n%!" x
let () = assert (x >= 0)                       (* raises Assert_failure (file, line, col) *)
let dbg fmt = Printf.ksprintf (fun s -> if Sys.getenv_opt "DEBUG" <> None then prerr_endline s) fmt
```
```bash
OCAMLRUNPARAM=b dune exec ./main.exe
dune utop        # then: #trace fn;;
```

## Notes
- `assert` is removed by `-noassert`; dune release profile does not remove it by default (unconfirmed), do not rely on side effects inside.
- `prerr_endline` flushes; `Printf.eprintf` needs `%!` or `flush stderr`.
- `Logs` library for structured log levels.
- `#trace` works in bytecode toplevel only.
- Debugging typing issues: ask Merlin for types, add annotations, or `ocamlfind ocamlc -i`.
- `dune build 2>&1 | head -50` keeps the first error in view.

## Self-check
- [ ] Debug prints appear before a crash because stderr was flushed.
