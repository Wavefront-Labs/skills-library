---
id: computing-software.software-engineering.ocaml.compiling-with-ocamlc-and-ocamlopt
name: compiling-with-ocamlc-and-ocamlopt
category: computing-software
field: software-engineering
product: ocaml
tags: [ocaml, ocamlc-ocamlopt, ocaml-toolchain, ocamlfind, ocamlopt, cmx-files, bytecode-native]
level: practitioner
status: docs-checked
description: "Compile and link by hand with ocamlc and ocamlopt, understand .cmi/.cmx/.cmo/.cmxa outputs and the -I, -g, -i and -bin-annot flags."
sources: ["https://ocaml.org/manual/", "https://ocaml.org/docs"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ocamlc / ocamlopt

```bash
ocamlopt -o prog util.mli util.ml main.ml
ocamlc -g -o prog.byte main.ml     # bytecode
ocamlopt -i main.ml                # print inferred interface
ocamlopt -c -I _build foo.ml
```

## Notes
- `ocamlc` makes bytecode (`.cmo`, `.cma`, run with `ocamlrun`); `ocamlopt` makes native code (`.cmx`, `.o`, `.cmxa`, `.a`). Each module's `.mli` compiles to `.cmi`.
- `-g` adds debug info, `-unsafe` removes bounds checks, `-w` selects warnings, `-bin-annot` writes `.cmt` files, `-i` prints the inferred interface, and `-I dir` adds a directory searched for `.cmi`, `.cmx` and `.cmxa` files.
- The manual's parallelism chapter builds a library program with `ocamlfind ocamlopt -package domainslib -linkpkg -o fib_par2.exe fib_par2.ml`; that findlib form is not part of the compiler chapters.
- Real projects should use dune; manual commands are for debugging builds.

## Self-check
- [ ] `ocamlopt -o x x.ml` produces a runnable executable.

## Checked

2026-11-03. Confirmed against the OCaml 5.5 manual: the ocamlc and ocamlopt chapters (.cmo/.cma, .cmx/.o/.cmxa/.a, .cmi from .mli, -g, -i, -I, -unsafe, -w, -bin-annot) and the parallelism chapter (ocamlfind -package/-linkpkg example).

Removed or corrected: ocamlfind-wrapped examples with unix/str packages, the dependency-order claim, the -O3 flambda remark, the Merlin remark, and ocamlfind list.

Method: documentation only; no commands were run.
