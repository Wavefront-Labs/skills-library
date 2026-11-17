---
id: computing-software.software-engineering.ocaml.stdlib-vs-base-and-core
name: stdlib-vs-base-and-core
category: computing-software
field: software-engineering
product: ocaml
tags: [ocaml, base-core, ocaml-ecosystem, base-library, core-library, jane-street, stdlib-alternative]
level: practitioner
status: docs-checked
description: "Choose between Stdlib, Jane Street Base and Containers; Base replaces the stdlib wholesale and removes polymorphic comparison."
sources: ["https://github.com/janestreet/base", "https://github.com/c-cube/ocaml-containers"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Stdlib vs Base vs Containers

## Choices
- **Stdlib**: ships with the compiler; the default environment.
- **Base** (Jane Street): a standard library meant as a wholesale replacement of the compiler's stdlib. It is well tested, performant and fully portable, and does not re-export non-portable features such as I/O (left to other libraries, e.g. Stdio). Base has no runtime dependencies.
- **Containers** (c-cube): an extension of the stdlib focused on data structures, combinators and iterators, with no dependency on unix, str or num. Modules are independent and prefixed `CC`; `open Containers` brings enhanced versions of the standard modules into scope.

```ocaml
open Base
let eq = List.equal String.equal [ "a" ] [ "a" ]     (* type-specific equality *)
let c = List.compare String.compare [ "a" ] [ "b" ]
let p = Stdlib.print_string "still reachable via Stdlib"
```

## Notes
- After `open Base`, everything the stdlib provides in the default environment is deprecated; reach the stdlib through the top-level name `Stdlib` (`Stdlib.String`, `Stdlib.print_string`).
- Polymorphic comparison is not exposed by Base: the default comparison operators are the integer ones. Use the `Poly` module for polymorphic comparison, or per-type `compare` functions; `ppx_compare` offers `[%compare: string list] x y`.
- Containers 2.0 and later also shadow the polymorphic operators with monomorphic ones under `open Containers`; get the old behaviour back with `Stdlib.(=)` or `open Stdlib` after it. Reason: structural comparison of maps and hashtables can give wrong results where semantic comparison is meant.
- Most Base types have `sexp_of_t` / `t_of_sexp`; `String.sexp_of_t` (a string embedded in a sexp) differs from `Sexp.to_string` (textual form).
- Pick one convention per codebase; do not mix idioms within a file.

## Self-check
- [ ] A file uses either Stdlib or Base conventions consistently.

## Checked

2026-11-08. Read in full: Base README.org and the ocaml-containers README.
Removed: claims about Core contents, Batteries, Base argument labels and `Or_error`, `String.split ~on`, and library-minimisation advice (not in cited pages); ocaml.org landing sources.
Method: documentation only; no commands were run.
