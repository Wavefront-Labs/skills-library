---
id: computing-software.software-engineering.ocaml.using-ppx-deriving-and-attributes
name: using-ppx-deriving-and-attributes
category: computing-software
field: software-engineering
product: ocaml
tags: [ocaml, ppx-deriving-usage, ocaml-ppx, ppx-deriving, deriving-show, attributes, extension-nodes]
level: practitioner
status: draft
description: "Derive show, eq, ord, hash with [@@deriving], add attributes and extension nodes, and enable the ppx in dune preprocess."
sources: ["https://ocaml-ppx.github.io/ppxlib/", "https://ocaml.org/manual/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Using ppx_deriving

```lisp
(library (name m) (preprocess (pps ppx_deriving.show ppx_deriving.eq ppx_deriving.ord)))
```
```ocaml
type color = Red | Green [@@deriving show, eq, ord]
type t = { id : int; name : string [@opaque]; c : color } [@@deriving show { with_path = false }]
let () = print_endline (show_color Red); Format.printf "%a@." pp_t { id = 1; name = "n"; c = Green }
```

## Notes
- Generated: `pp_t`, `show_t`, `equal_t`, `compare_t`; for a type named `t` the functions are `pp`, `show`, `equal`, `compare`.
- Syntax: `[@@deriving x]` attaches to a type; `[%e]` extension nodes (e.g. `let%expect_test`, `[%expect]`); `[@attr]` attributes on expressions; `[@@attr]` on items; `[@@@attr]` floating.
- `ppx_jane` bundles Jane Street ppxes (sexp, compare, hash, inline_test, ...).
- Rule of thumb: derive only what you use; ppx adds build time and obscures errors.
- Run `dune describe pp file.ml` or `ocamlfind ppx_tools/rewriter` to see expanded code (use `dune describe pp` where available).

## Self-check
- [ ] `show_color Red` prints the constructor name.
