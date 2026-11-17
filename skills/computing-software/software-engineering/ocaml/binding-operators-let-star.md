---
id: computing-software.software-engineering.ocaml.binding-operators-let-star
name: binding-operators-let-star
category: computing-software
field: software-engineering
product: ocaml
tags: [ocaml, binding-operators, let-operators, monadic-binding, and-star]
level: advanced
status: gated
description: "Define let*, let+, and* operators for options, results, and monads in Stdlib style; scope them with local opens."
sources: ["https://ocaml.org/manual/", "https://dev.realworldocaml.org/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Binding operators

```ocaml
module Option_syntax = struct
  let ( let* ) = Option.bind
  let ( let+ ) o f = Option.map f o
  let ( and+ ) a b = match a, b with Some x, Some y -> Some (x, y) | _ -> None
end
let add a b = Option_syntax.(
  let+ x = a and+ y = b in x + y)        (* Some 3 for Some 1, Some 2 *)
```

## Notes
- Available since OCaml 4.08. `let*`/`let+` desugar to the operator applied to the bound expression and a function; `and*`/`and+` combine parallel bindings.
- Operator name is `let` or `and` followed by operator characters; define only those you use.
- Scope them with `let open Syntax in` or `Syntax.( ... )` to avoid polluting; Lwt and Eio expose `Lwt.Syntax` (`let*`, `let+`), `Lwt.Infix`.
- Error messages mention the desugared bind; check the operator's type if you see surprising unification errors.
- `match%lwt`/`let%lwt` are ppx_lwt alternatives; with binding operators no ppx is needed.

## Self-check
- [ ] Code with `let*` over Lwt promises compiles without ppx.

## Checked

- Date: 2026-11-02.
- Source pages listed in `sources` were fetched where possible; the manual root was fetched but not the binding-operators chapter; Lwt.Syntax and ppx_lwt claims not checked. Treat the specific names, flags and figures as unconfirmed (gated: unconfirmed, source is paywalled or blocked).

Method: documentation only; no commands were run.
