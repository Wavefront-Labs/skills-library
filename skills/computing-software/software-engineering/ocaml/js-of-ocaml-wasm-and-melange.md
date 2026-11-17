---
id: computing-software.software-engineering.ocaml.js-of-ocaml-wasm-and-melange
name: js-of-ocaml-wasm-and-melange
category: computing-software
field: software-engineering
product: ocaml
tags: [ocaml, js-of-ocaml-melange, js-of-ocaml, melange, wasm-of-ocaml, browser-ocaml]
level: advanced
status: docs-checked
description: "Compile OCaml to JavaScript with js_of_ocaml (from bytecode) or Melange (compiler fork), and know wasm_of_ocaml; choose per runtime."
sources: ["https://github.com/ocsigen/js_of_ocaml", "https://github.com/melange-re/melange"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OCaml for the browser

```bash
opam install js_of_ocaml js_of_ocaml-compiler js_of_ocaml-ppx
ocamlfind ocamlc -package js_of_ocaml -package js_of_ocaml-ppx -linkpkg -o cubes.byte cubes.ml
js_of_ocaml cubes.byte
```

## Notes
- js_of_ocaml is a compiler from OCaml bytecode to JavaScript: your program is first compiled with `ocamlc`, then `js_of_ocaml` produces the JS. It works with an existing OCaml installation without recompiling libraries. Packages: `js_of_ocaml-compiler`, `js_of_ocaml-ppx`, `js_of_ocaml` (bindings for browser APIs), `-lwt`, `-tyxml`, `-toplevel`, and `wasm_of_ocaml-compiler`.
- Generated code targets ES2020 and runs on Node.js 18 or later and evergreen browsers; older engines need transpiling to ES5. `wasm_of_ocaml-compiler` additionally needs a system binaryen (version 120 or later).
- Most of the standard library works; most of `Sys` does not, and extra libraries like Thread are generally unsupported. Bigarray, Num and Str are supported; Unix only time-related functions.
- Data representation differs: `int` is a 32-bit JS number, floats are unboxed, so marshalling, polymorphic hash and comparison can give different results. Tail calls are not optimised in general: self-recursive functions become loops, others use trampolines. Effect handlers need `--effects={cps,double-translation}`.
- Melange compiles OCaml and Reason to JavaScript; it is a fork of the ReScript compiler focused on integration with the OCaml ecosystem (Dune virtual libraries share code between backend and frontend). Install with `opam install melange`; it has first-class Dune support; see melange.re to start.
- Melange version compatibility: v3.0 on OCaml 4.14 and 5.1, v2.0 on 5.1 only, v1.0 on 4.13 or later. The ReScript compatibility layer was removed in 2.0.

## Self-check
- [ ] The generated JS runs in a browser or Node.

## Checked

2026-11-08. Read in full: js_of_ocaml README and Melange README.
Removed: dune stanzas, `##` binding syntax, `[@mel.module]`/`[@mel.send]` attributes, `melange.emit`, and the "pick X for Y" recommendation (not in the cited pages).
Method: documentation only; no commands were run.
