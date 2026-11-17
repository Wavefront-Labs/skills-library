---
id: computing-software.software-engineering.ocaml.merlin-code-navigation-and-holes
name: merlin-code-navigation-and-holes
category: computing-software
field: software-engineering
product: ocaml
tags: [ocaml, merlin-features, merlin-destruct, merlin-construct, typed-holes, type-driven]
level: practitioner
status: docs-checked
description: "Use OCaml-LSP typed holes (_), destruct, construct and switch implementation/interface to write code type-first."
sources: ["https://raw.githubusercontent.com/ocaml/ocaml-lsp/master/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Type-driven editing with OCaml-LSP

```ocaml
type t = A | B of string option
let f (v : t) = match v with | A -> _ | B _ -> _   (* each _ is a typed hole *)
```

## Notes
- A typed hole is `_` in place of an expression, e.g. `let foo : int = _` (type `int`) or `let bar = _ 10` (type `int -> 'a`). Holes are temporary substitutes you plug later. A file with holes is not valid OCaml and cannot be compiled. A `_` in pattern position (`let _ = 10`) is not a hole.
- Destruct (since OCaml-LSP 1.0.0): a code action that generates an exhaustive pattern match for a value. It works only when the value's precise type is inferable, so annotate a polymorphic parameter first (`let f (v : t) = ...`). It also works on the `_` pattern inside a match. VS Code OCaml Platform binds it to Alt+D (Option+D on macOS).
- Construct (experimental, since 1.8.0): typing `_` where an expression is required triggers completion offering values of the required type (e.g. `Foo.A`, `Foo.B _`); the code action "Construct an expression" refines a hole further. The type must be non-polymorphic. VS Code binding: Alt+C (Option+C on macOS).
- LSP extensions: switch to implementation/interface, infer interface, locate typed holes, find wrapping AST node. Editor support for these varies; VS Code's OCaml Platform has the best.
- Generated code may be poorly formatted; run OCamlFormat, which supports typed holes.
- Syntax documentation on hover is optional (since 1.18.0): enable with the `syntaxDocumentation` config key set to `{ enable: true }`.

## Self-check
- [ ] The code action menu offers Destruct on a variant-typed expression.

## Checked
Date: 2026-11-08. Confirmed against the ocaml-lsp README on GitHub (read in full). Removed: the length example with Merlin completion claims, "holes compile with a warning", Locate via `.cmt` with `-bin-annot`, docs-comment hover, the partial-parse-tree claim, and the ocaml.org/docs and Merlin site sources (not read).
Method: documentation only; no commands were run.
