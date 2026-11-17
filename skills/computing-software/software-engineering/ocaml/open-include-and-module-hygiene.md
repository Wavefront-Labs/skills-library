---
id: computing-software.software-engineering.ocaml.open-include-and-module-hygiene
name: open-include-and-module-hygiene
category: computing-software
field: software-engineering
product: ocaml
tags: [ocaml, module-open-include, local-open, module-alias, include, open-shadowing]
level: practitioner
status: docs-checked
description: "Avoid global open, use local opens and module aliases, and understand includes and Stdlib name shadowing."
sources: ["https://ocaml.org/manual/", "https://dev.realworldocaml.org/", "https://github.com/ocaml/ocaml/tree/trunk/stdlib", "https://github.com/ocaml/ocaml/tree/trunk/manual/src"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# open / include hygiene

```ocaml
let x = List.(map succ [1;2])        (* local open of List *)
let y = let open String in length "ab"
module L = List                      (* alias *)
module List_ext = struct include List let sum = fold_left ( + ) 0 end
```

## Rules
- Global `open Foo` pollutes scope; a value added to `Foo` later can shadow your names silently. Warnings 44/45 (open shadows identifier/label) catch this; enable them.
- `open!` suppresses the unused-open warning (33) and the shadowing warnings (44/45).
- `include` re-exports; in an `.mli`, `include module type of M` copies a module's signature.

## Self-check
- [ ] `-w +44+45` raises no warnings in your code, or each open is justified.

## Checked
2026-11-02. Confirmed: local open syntax, warnings 33/44/45 (warnings.ml), `open!` (manual overriding open), `module type of` (manual). Removed: Jane Street style claim.
Method: documentation only (OCaml stdlib .mli files and manual .etex sources from github.com/ocaml/ocaml, trunk); no commands were run.
