---
id: computing-software.software-engineering.ocaml.tuples-and-records
name: tuples-and-records
category: computing-software
field: software-engineering
product: ocaml
tags: [ocaml, tuples-records, record-fields, record-with, record-punning, mutable-field]
level: intro
status: docs-checked
description: "Define records with mutable fields, punning, with-copy and field disambiguation; destructure tuples; know record label clashes."
sources: ["https://ocaml.org/manual/", "https://ocaml.org/docs", "https://github.com/ocaml/ocaml/tree/trunk/stdlib", "https://github.com/ocaml/ocaml/tree/trunk/manual/src"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tuples and records

```ocaml
let p = (1, "a")   let (n, s) = p   let n = fst p
type user = { name : string; mutable age : int }
let u = { name = "ann"; age = 30 }
u.age <- 31                          (* mutable field *)
let u2 = { u with name = "bob" }     (* copy with change *)
let mk name age = { name; age }      (* punning *)
```

## Notes
- Records are nominal: the latest-defined record with a given label wins, so two types with a `name` field cause type errors. Annotate: `(u : user)` or write `u.User.name`.
- Warnings 40/41/42 relate to type-directed label disambiguation.
- Mutability is per field; there is no per-record immutability keyword.
- `{ u with ... }` allocates a new record; it does not mutate.

## Gotchas
- Pattern matching a record without listing all fields triggers warning 9 unless you end with `; _`.

## Self-check
- [ ] Two records sharing a field name are in separate modules or annotated.

## Checked
2026-11-02. Confirmed: record syntax, mutable fields, `with`, punning, label disambiguation warnings 9/40/41/42 (manual and warnings.ml). Removed: convention remark.
Method: documentation only (OCaml stdlib .mli files and manual .etex sources from github.com/ocaml/ocaml, trunk); no commands were run.
