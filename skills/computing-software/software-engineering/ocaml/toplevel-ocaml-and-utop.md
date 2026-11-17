---
id: computing-software.software-engineering.ocaml.toplevel-ocaml-and-utop
name: toplevel-ocaml-and-utop
category: computing-software
field: software-engineering
product: ocaml
tags: [ocaml, toplevel-utop, utop, toplevel-directives, dune-utop, ocaml-repl]
level: intro
status: docs-checked
description: "Use the ocaml toplevel: #use, #load, #directory, #show and #trace directives, .ocamlinit and script mode; utop is an improved toplevel."
sources: ["https://ocaml.org/manual/", "https://ocaml.org/docs"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Toplevel and utop

```bash
ocaml                      # basic REPL; end phrases with ;;
utop                       # an improved toplevel (separate program)
```
```ocaml
#use "script.ml";;                 #directory "_build/default";;
#show List;;                       #trace fib;;           #untrace_all;;
#use_output "cmd";;                #quit;;
```

## Notes
- `#use` runs a file as if typed; `#load "x.cma"` loads a bytecode object file; `#directory` adds a search directory.
- The toplevel looks for `.ocamlinit` in the current directory and in `HOME`; keep it small.
- In script mode `ocaml script.ml` runs a file directly and the first line is ignored if it starts with `#!`. Because `ocaml` is itself a `#!` script on most installations, the manual suggests `#!/usr/local/bin/ocamlrun /usr/local/bin/ocaml` as the first line.

## Self-check
- [ ] `#use "script.ml";;` loads the file and its definitions are usable afterwards.

## Checked

2026-11-03. Confirmed against the OCaml 5.5 manual: the toplevel chapter (#use, #load, #directory, #show, #trace, #untrace_all, #use_output, #quit, .ocamlinit lookup, script mode and the #! advice, utop mentioned as an improved toplevel).

Removed or corrected: all dune utop and dune ocaml top-module content, #require and topfind (findlib, not in the manual), the opam install command and the last-value remark.

Method: documentation only; no commands were run.
