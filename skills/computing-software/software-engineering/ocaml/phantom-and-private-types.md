---
id: computing-software.software-engineering.ocaml.phantom-and-private-types
name: phantom-and-private-types
category: computing-software
field: software-engineering
product: ocaml
tags: [ocaml, phantom-private-types, phantom-types, private-types, abstract-types-invariants]
level: advanced
status: docs-checked
description: "Encode state in phantom parameters and use private type abbreviations/records to enforce invariants at API boundaries."
sources: ["https://ocaml.org/manual/", "https://dev.realworldocaml.org/", "https://github.com/ocaml/ocaml/tree/trunk/stdlib", "https://github.com/ocaml/ocaml/tree/trunk/manual/src"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Phantom and private types

```ocaml
(* units.mli *)
type 'unit t
type meters and feet
val meters : float -> meters t
val add : 'u t -> 'u t -> 'u t
(* units.ml *)
type 'unit t = float
type meters and feet
let meters x = x
let add = ( +. )
```

```ocaml
module Email : sig
  type t = private string            (* readable via coercion, constructible only here *)
  val of_string : string -> t option
end = struct
  type t = string
  let of_string s = if String.contains s '@' then Some s else None
end
let s : string = (e :> string)       (* coercion allowed for private abbreviations *)
```

## Notes
- Phantom parameters appear in the type but not the representation; the `.mli` must keep the type abstract.
- `private` variant/record types permit matching/reading but not construction outside the module.

## Self-check
- [ ] Adding `meters t` to `feet t` is a type error.

## Checked
2026-11-02. Confirmed: private type abbreviations and coercion `(x :> string)`; private variants/records (manual private types). Removed: variance remark.
Method: documentation only (OCaml stdlib .mli files and manual .etex sources from github.com/ocaml/ocaml, trunk); no commands were run.
