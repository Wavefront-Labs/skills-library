---
id: computing-software.software-engineering.ocaml.structural-object-types
name: structural-object-types
category: computing-software
field: software-engineering
product: ocaml
tags: [ocaml, object-rows, object-types, row-polymorphism, immediate-objects]
level: advanced
status: docs-checked
description: "Use object types < m : t; .. > with row variables, immutable-object updates ({< >}) and coercions for duck-typing."
sources: ["https://ocaml.org/manual/", "https://github.com/ocaml/ocaml/tree/trunk/stdlib", "https://github.com/ocaml/ocaml/tree/trunk/manual/src"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Structural object types

```ocaml
let area_of (s : < area : float; .. >) = s#area       (* any object with area *)
let o = object method area = 2.0 method name = "sq" end
let _ = area_of o
let point = object val x = 0 method move d = {< x = x + d >} end   (* functional update *)
```

## Notes
- `..` is a row variable; a closed type `< area : float >` accepts only objects with exactly that interface (coerce down with `:>`).
- `{< x = e >}` returns a copy of self with updated instance variables.
- Binary methods and `self` types need explicit type annotations.

## Self-check
- [ ] Passing an object missing the method fails type-checking.

## Checked
2026-11-02. Confirmed: object types with row variable `..`, `{< >}` functional update, coercion (manual objects tutorial and classes chapter). Removed: error-message wording and Real World OCaml advice.
Method: documentation only (OCaml stdlib .mli files and manual .etex sources from github.com/ocaml/ocaml, trunk); no commands were run.
