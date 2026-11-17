---
id: computing-software.software-engineering.ocaml.extensible-variants-and-exceptions
name: extensible-variants-and-exceptions
category: computing-software
field: software-engineering
product: ocaml
tags: [ocaml, extensible-variants, extensible-variant, type-extension, exn-type]
level: advanced
status: docs-checked
description: "Define open types with type t = .. and add constructors across modules; relate to exn, and handle matching on open types."
sources: ["https://ocaml.org/manual/", "https://dev.realworldocaml.org/", "https://github.com/ocaml/ocaml/tree/trunk/stdlib", "https://github.com/ocaml/ocaml/tree/trunk/manual/src"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Extensible variants

```ocaml
type event = ..
type event += Click of int * int
type event += Key of char
let describe = function
  | Click (x, y) -> Printf.sprintf "click %d,%d" x y
  | Key c -> Printf.sprintf "key %c" c
  | _ -> "other"                      (* a catch-all is mandatory *)
```

## Notes
- `exn` is the built-in extensible variant; `exception E of int` is `type exn += E of int`.
- Matching on an extensible type requires a default (wildcard) case to handle unknown constructors.
- Register a printer with `Printexc.register_printer` (`(exn -> string option) -> unit`) for readable messages from custom exceptions.
- Prefer ordinary variants when the set is closed.

## Self-check
- [ ] Printing an uncaught custom exception shows a readable message (a registered `Printexc` printer).

## Checked
2026-11-02. Confirmed: `..` and `+=`, mandatory default case, exn as extensible type (manual extensible variants), Printexc.register_printer signature. Removed: no-exhaustiveness-check, plugin and generativity claims, `[@@deriving]`.
Method: documentation only (OCaml stdlib .mli files and manual .etex sources from github.com/ocaml/ocaml, trunk); no commands were run.
