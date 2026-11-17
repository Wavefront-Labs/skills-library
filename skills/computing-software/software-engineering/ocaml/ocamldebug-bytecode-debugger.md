---
id: computing-software.software-engineering.ocaml.ocamldebug-bytecode-debugger
name: ocamldebug-bytecode-debugger
category: computing-software
field: software-engineering
product: ocaml
tags: [ocaml, ocamldebug, ocaml-debugging, bytecode-debugger, time-travel-debugging]
level: advanced
status: docs-checked
description: "Debug bytecode with ocamldebug: build with -g, step, break, backtrace, and time travel through fork-based checkpoints."
sources: ["https://ocaml.org/manual/", "https://ocaml.org/docs"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ocamldebug

```bash
ocamlc -g -o prog.byte main.ml
ocamldebug ./prog.byte
(ocd) break @ Main 12     (ocd) run     (ocd) next     (ocd) step     (ocd) print x
(ocd) backtrace    (ocd) frame 1    (ocd) reverse    (ocd) last
```

## Notes
- The program must be compiled and linked with `ocamlc -g`; `-g` does not slow the running program.
- Time travel (`reverse`, `backstep`, `goto`) relies on checkpoints, which are copies of the program state made with the Unix `fork` call; `set checkpoints off` disables them.
- Printing: `print`, `display`, `set print_depth`; `info breakpoints`.

## Self-check
- [ ] A breakpoint at a function entry stops and shows its arguments.

## Checked

2026-11-03. Confirmed against the OCaml 5.5 manual: the debugger chapter (-g requirement and no running-time penalty, break @ module line, run, next, step, print, display, set print_depth, backtrace, frame, reverse, backstep, last, goto, info breakpoints, fork-based checkpoints, set checkpoints).

Removed or corrected: dune main.bc instructions, the OCaml 5 limitation guess, and the native-debugging advice.

Method: documentation only; no commands were run.
