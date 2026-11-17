---
id: computing-software.software-engineering.ocaml.gadts-and-existential-types
name: gadts-and-existential-types
category: computing-software
field: software-engineering
product: ocaml
tags: [ocaml, gadts, ocaml-advanced-types, gadt, locally-abstract-types, existential-types, typed-ast]
level: advanced
status: docs-checked
description: "Declare GADTs for typed ASTs, use type a. locally abstract annotations on recursive functions, and existential packing."
sources: ["https://ocaml.org/manual/", "https://dev.realworldocaml.org/", "https://github.com/ocaml/ocaml/tree/trunk/stdlib", "https://github.com/ocaml/ocaml/tree/trunk/manual/src"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GADTs

```ocaml
type _ expr =
  | Int : int -> int expr
  | Bool : bool -> bool expr
  | Add : int expr * int expr -> int expr
  | If : bool expr * 'a expr * 'a expr -> 'a expr
let rec eval : type a. a expr -> a = function
  | Int n -> n
  | Bool b -> b
  | Add (x, y) -> eval x + eval y
  | If (c, t, e) -> if eval c then eval t else eval e
```

## Rules
- Functions matching on GADTs that refine the return type need an explicit polymorphic annotation: `type a. a expr -> a` (locally abstract type, explicit polymorphic recursion).
- Existentials: `type packed = Pack : 'a expr -> packed`; the hidden type cannot escape the match.
- The exhaustiveness check is aware of GADT constraints, so impossible cases need not be written.

## Self-check
- [ ] Omitting `type a.` yields the "this type would escape its scope / rigid type" error, which tells you annotation is required.

## Checked
2026-11-02. Confirmed: GADT syntax, locally abstract types and explicit polymorphic annotation, existential variables, GADT-aware exhaustiveness (manual GADT tutorial). Removed: spurious-error and warning 4 claims.
Method: documentation only (OCaml stdlib .mli files and manual .etex sources from github.com/ocaml/ocaml, trunk); no commands were run.
