---
id: computing-software.software-engineering.ocaml.monad-and-applicative-patterns
name: monad-and-applicative-patterns
category: computing-software
field: software-engineering
product: ocaml
tags: [ocaml, monad-patterns, monad, state-monad, applicative, higher-kinded-types]
level: advanced
status: draft
description: "Define return/bind (state, reader, parser, result) with module signatures and let* syntax, and know what higher-kinded limits mean."
sources: ["https://dev.realworldocaml.org/", "https://ocaml.org/docs"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Monads in OCaml

```ocaml
module type MONAD = sig
  type 'a t
  val return : 'a -> 'a t
  val bind : 'a t -> ('a -> 'b t) -> 'b t
end
module State = struct
  type ('s, 'a) t = 's -> 'a * 's
  let return a s = (a, s)
  let bind m f s = let (a, s') = m s in f a s'
  let ( let* ) = bind
  let get s = (s, s)    let put s _ = ((), s)
end
```

## Notes
- OCaml has no higher-kinded types, so generic code over every monad needs functors (`module Make (M : MONAD)`), not type constructors as parameters.
- Define `let*`/`let+`/`and+` once per monad.
- Idiomatic OCaml often uses plain mutable state, exceptions or effects instead of monads; reach for monads in parsers, promises (Lwt), and result chaining.
- Laws: left identity, right identity, associativity; test them with property tests.
- Jane Street's Base provides `Monad.S` and `Monad.Make` for ready-made helpers.

## Self-check
- [ ] State monad counter increments across three binds.
