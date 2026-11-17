---
id: computing-software.software-engineering.ocaml.polymorphic-variants
name: polymorphic-variants
category: computing-software
field: software-engineering
product: ocaml
tags: [ocaml, polymorphic-variants, polymorphic-variant, open-variant, closed-variant]
level: advanced
status: docs-checked
description: "Use backtick polymorphic variants with open [> ] and closed [< ] types, and know when plain variants are safer."
sources: ["https://ocaml.org/manual/", "https://dev.realworldocaml.org/", "https://github.com/ocaml/ocaml/tree/trunk/stdlib", "https://github.com/ocaml/ocaml/tree/trunk/manual/src"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Polymorphic variants

```ocaml
let c = `Red                         (* [> `Red ] *)
let name = function `Red -> "r" | `Green -> "g"   (* [< `Green | `Red ] -> string *)
type color = [ `Red | `Green ]
type more = [ color | `Blue ]        (* inheritance *)
```

## Notes
- No declaration needed; types are structural with row variables (`[> ...]` open, `[< ...]` closed).
- Useful for error sets: return `(_, [> `Not_found | `Io of string]) result` that callers extend.
- Costs: `[> ]` types can leak into interfaces; an open `[> ...]` type accepts tags you did not intend.
- Coerce a `color` to `more` with `(x :> more)`.
- Prefer regular variants for core domain types; use polymorphic variants for open sets (errors, events).

## Self-check
- [ ] Interfaces constrain with explicit `[ ... ]` types, not inferred `[> ...]` leaks.

## Checked
2026-11-02. Confirmed: `[> ]`/`[< ]` types, inheritance, coercion (manual polymorphic variants tutorial). Removed: error-message and typo claims.
Method: documentation only (OCaml stdlib .mli files and manual .etex sources from github.com/ocaml/ocaml, trunk); no commands were run.
