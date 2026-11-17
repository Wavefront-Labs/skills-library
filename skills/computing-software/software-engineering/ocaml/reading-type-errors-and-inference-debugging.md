---
id: computing-software.software-engineering.ocaml.reading-type-errors-and-inference-debugging
name: reading-type-errors-and-inference-debugging
category: computing-software
field: software-engineering
product: ocaml
tags: [ocaml, type-error-reading, type-errors, error-messages, annotation-debugging, syntax-errors]
level: practitioner
status: draft
description: "Decode OCaml type errors, find first-mismatch locations, use annotations, -principal and labels, and fix common causes (missing rec, parentheses, semicolons)."
sources: ["https://ocaml.org/manual/api/", "https://ocaml.org/docs"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Reading OCaml errors

## Strategy
1. Fix the first error only; later ones often cascade.
2. For "This expression has type A but an expression was expected of type B": the expression marked is where inference gave up. Annotate the surrounding function's parameters and return type to localise.
3. For "Error: Syntax error": look just before the marked token for a missing `in`, `;;`, `)` or stray `;` before `else`/`|`.
4. "Unbound value x": missing `rec`, wrong module, or the library is not in `(libraries ...)`.
5. "This pattern matches values of type ..." shows constructor type mismatches.
6. "The type of this expression contains type variables that cannot be generalized": value restriction (see value-restriction-and-weak-types).
7. "Warning 8 [partial-match]" lists missing cases.

## Tools
- Merlin type-at-cursor; `dune build 2>&1` shows the full message with `^^^` markers.
- `ocamlfind ocamlc -i x.ml` shows inferred interface.
- `-short-paths` flag makes types shorter in errors; `-principal` reports unsafe inference (rarely needed).

## Self-check
- [ ] The first reported error is the one you fix.
