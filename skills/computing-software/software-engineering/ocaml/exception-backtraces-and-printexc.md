---
id: computing-software.software-engineering.ocaml.exception-backtraces-and-printexc
name: exception-backtraces-and-printexc
category: computing-software
field: software-engineering
product: ocaml
tags: [ocaml, backtraces, ocamlrunparam-b, printexc, backtrace, exception-printer]
level: practitioner
status: docs-checked
description: "Enable backtraces with OCAMLRUNPARAM=b or Printexc.record_backtrace, print with Printexc.get_backtrace, and register custom exception printers."
sources: ["https://ocaml.org/manual/", "https://dev.realworldocaml.org/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Backtraces

```bash
OCAMLRUNPARAM=b ./main.exe        # print backtrace of uncaught exception
```
```ocaml
let () = Printexc.record_backtrace true
let () =
  try risky () with e ->
    let bt = Printexc.get_raw_backtrace () in   (* capture immediately *)
    prerr_endline (Printexc.to_string e);
    Printexc.print_raw_backtrace stderr bt;
    Printexc.raise_with_backtrace e bt           (* re-raise preserving trace *)
let () = Printexc.register_printer (function Parse_error s -> Some ("parse: " ^ s) | _ -> None)
```

## Notes
- Compile with `-g`: the ocamlrun manual says the bytecode back trace is printed only if the executable contains debugging information.
- `Printexc.exn_slot_id` and `Printexc.use_printers` also exist.
- Backtraces are not recorded unless `b` is in `OCAMLRUNPARAM` or `Printexc.record_backtrace true` is called.

## Self-check
- [ ] A crash prints a backtrace with locations.

## Checked

2026-11-03. Confirmed against the OCaml 5.5 manual: the Printexc API (record_backtrace, get_raw_backtrace, print_raw_backtrace, raise_with_backtrace, register_printer, use_printers, exn_slot_id) and the ocamlrun page (b flag, -g requirement).

Removed or corrected: dune commands and dune profile claims, the flambda trace remark, the OCaml 5 re-raise claim, the Raised-at output format, and the claim that b works for native code in particular.

Method: documentation only; no commands were run.
