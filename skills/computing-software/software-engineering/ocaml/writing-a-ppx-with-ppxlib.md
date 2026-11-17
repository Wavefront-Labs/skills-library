---
id: computing-software.software-engineering.ocaml.writing-a-ppx-with-ppxlib
name: writing-a-ppx-with-ppxlib
category: computing-software
field: software-engineering
product: ocaml
tags: [ocaml, ppxlib-write, ppxlib, metaquot, ppx-deriver, ast-rewriting]
level: advanced
status: draft
description: "Author a deriver or extension rewriter using ppxlib Deriving.add, metaquot, and test with dune; list common pitfalls."
sources: ["https://ocaml-ppx.github.io/ppxlib/", "https://ocaml.org/manual/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Writing a ppx with ppxlib

```lisp
(library (name ppx_hello) (kind ppx_deriver) (libraries ppxlib) (preprocess (pps ppxlib.metaquot)))
```
```ocaml
open Ppxlib
let expand ~ctxt =
  let loc = Expansion_context.Extension.extension_point_loc ctxt in
  [%expr "hello"]
let ext = Extension.V3.declare "hello" Extension.Context.expression Ast_pattern.(pstr nil) expand
let () = Driver.register_transformation "hello" ~rules:[ Context_free.Rule.extension ext ]
```

## Notes
- Skeleton only; API shapes (Extension.V3, Deriving.add with generators) vary by ppxlib version: follow the ppxlib manual's "Writing a ppx" and the examples in the repo.
- `ppxlib.metaquot` provides `[%expr ...]`, `[%stri ...]`, `[%type: ...]`, with `$e$` antiquotations.
- Locations: always propagate `~loc` so error messages point at the user's code; use `Location.raise_errorf ~loc`.
- Derivers register via `Deriving.add "name" ~str_type_decl:(...)`.
- Test with dune expect/cram tests that print `dune describe pp` output.
- All ppxes run in a single driver; ordering and name clashes are managed by ppxlib.

## Self-check
- [ ] An error in user code is reported at the correct source location.
