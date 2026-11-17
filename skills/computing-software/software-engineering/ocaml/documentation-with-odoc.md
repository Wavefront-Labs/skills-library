---
id: computing-software.software-engineering.ocaml.documentation-with-odoc
name: documentation-with-odoc
category: computing-software
field: software-engineering
product: ocaml
tags: [ocaml, odoc-docs, ocaml-docs-style, odoc, doc-comments, dune-build-doc, odoc-markup]
level: practitioner
status: docs-checked
description: "Write (** ... *) doc comments with odoc markup and tags, add .mld pages, and build docs via dune build @doc."
sources: ["https://ocaml.github.io/odoc/odoc/odoc_for_authors.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# odoc

```ocaml
(** [add a b] is the sum of [a] and [b].
    @raise Invalid_argument if the result overflows.
    @since 0.2 *)
val add : int -> int -> int
(** {1 Section}
    {[ let x = add 1 2 ]}  code block
    - bullet {!Mylib.add} reference, {{: https://ocaml.org} link} *)
```
```bash
dune build @doc          # output in _build/default/_doc/_html/index.html
```

## Notes
- Doc comments have exactly two asterisks. A comment attaches to an element when it sits immediately before or after it with no blank line; a comment between two elements is ambiguous and attaches to both, so use a blank line to clarify (dune raises an error for ambiguous comments in source files).
- Markup: `{b}` bold, `{i}` italic, `{e}` emphasis, `[code]`, `{[ ... ]}` code block, `{v ... v}` verbatim, `{!Foo.bar}` references, `{{: url } text}` links, `{ul {- ...}}` / `{ol {- ...}}` lists with `-` and `+` shorthand (ends at a blank line).
- Headings: `{0 Title}` for page titles only, `{1}` to `{5}` for sections; labels as `{2:label Title}`.
- Tags: line tags `@author @since @version @canonical`; block tags `@param <id>`, `@return`, `@raise`, `@see`, `@deprecated`, `@before` (block tags end at a blank line).
- Pages are `.mld` files; a package's `doc/index.mld` starts with `{0 Title}`, other `.mld` files in `doc/` are included automatically. `{!modules: A B C}` lists links to modules with their synopses.

## Self-check
- [ ] `dune build @doc` completes with no warnings.

## Checked
Checked 2026-11-08 against the odoc authoring reference. Removed: warning 50, `@doc-private`, the `opam install odoc` and mdx lines, and the `{{!ref} text}` form (not on the page). Corrected the link syntax to `{{: url } text}`. Unchanged: the (** *) syntax, tags, `.mld`, `@doc` output path.

Method: documentation only; no commands were run.
