---
id: computing-software.software-engineering.ocaml.functions-currying-and-application
name: functions-currying-and-application
category: computing-software
field: software-engineering
product: ocaml
tags: [ocaml, functions-currying, currying, partial-application, pipe-operator]
level: intro
status: docs-checked
description: "Define functions with fun/function, understand currying and partial application, and use |> and @@ for readable chains."
sources: ["https://ocaml.org/manual/", "https://ocaml.org/docs", "https://github.com/ocaml/ocaml/tree/trunk/stdlib", "https://github.com/ocaml/ocaml/tree/trunk/manual/src"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Functions, currying, partial application

```ocaml
let add x y = x + y            (* int -> int -> int *)
let incr1 = add 1              (* partial application *)
let f = fun x -> x * 2
let g = function 0 -> "zero" | _ -> "other"   (* fun + match on the one argument *)
let r = [1;2;3] |> List.map incr1 |> List.filter (fun x -> x > 2)
let s = String.concat "," @@ List.map string_of_int [1;2]
```

## Notes
- Every function takes one argument; `a -> b -> c` is `a -> (b -> c)`. The order in which
  arguments are evaluated is not specified (manual): never rely on it.
- `|>` is `x |> f = f x`; `@@` is `f @@ x = f x` and is right associative.
- `Fun.id`, `Fun.const`, `Fun.flip`, `Fun.negate` exist in Stdlib.Fun.
- Tuples vs curried: `let f (x, y)` takes one tuple; prefer curried for partial application.
- `let f a = function ...` is the idiom when the last argument is matched.

## Gotchas
- `let f () = ...` delays evaluation; a bare `let x = f ()` at top level runs at module initialisation.
- Side effects before the returned `fun` run at partial-application time, once.

## Self-check
- [ ] In `ocaml`, `let inc = add 1;; inc 2` evaluates to 3.

## Checked
2026-11-02. Confirmed: unspecified argument evaluation order (manual expr), `|>`/`@@` associativity and `Fun` functions (stdlib.mli, fun.mli). Removed: 'right-to-left in practice with ocamlopt'.
Method: documentation only (OCaml stdlib .mli files and manual .etex sources from github.com/ocaml/ocaml, trunk); no commands were run.
