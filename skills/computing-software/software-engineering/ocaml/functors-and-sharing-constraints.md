---
id: computing-software.software-engineering.ocaml.functors-and-sharing-constraints
name: functors-and-sharing-constraints
category: computing-software
field: software-engineering
product: ocaml
tags: [ocaml, functors, functor, map-make, set-make, sharing-constraint, first-class-module]
level: advanced
status: docs-checked
description: "Build functors (Map.Make, Set.Make, custom), apply sharing constraints with type t = ..., and use first-class modules when needed."
sources: ["https://ocaml.org/manual/", "https://dev.realworldocaml.org/", "https://github.com/ocaml/ocaml/tree/trunk/stdlib", "https://github.com/ocaml/ocaml/tree/trunk/manual/src"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Functors

```ocaml
module String_map = Map.Make (String)
module Int_set = Set.Make (Int)
let m = String_map.(empty |> add "a" 1 |> add "b" 2)

module type KEY = sig type t val compare : t -> t -> int end
module Make (K : KEY) = struct
  type key = K.t
  let sort l = List.sort K.compare l
end
module Sorter = Make (struct type t = int let compare = compare end)
```

## Notes
- A functor is a function from modules to modules.
- Result signatures need sharing: `module Make (K : KEY) : S with type key = K.t`; otherwise `key` is abstract.
- A functor taking `()` is generative: types it defines differ per application (manual, generative functors).
- First-class modules: `(module M : S)` packs, `(val m : S)` unpacks; useful for runtime-selected implementations.

## Self-check
- [ ] `String_map.find_opt "a" m` returns `Some 1` in a toplevel.

## Checked
2026-11-02. Confirmed: functor syntax and generative functors (manual), first-class module pack/unpack `(module M : S)`/`(val m : S)`. Removed: applicative-by-default claim, evaluation-time claim, Map.Make compare/equality claim.
Method: documentation only (OCaml stdlib .mli files and manual .etex sources from github.com/ocaml/ocaml, trunk); no commands were run.
