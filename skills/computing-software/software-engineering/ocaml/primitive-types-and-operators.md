---
id: computing-software.software-engineering.ocaml.primitive-types-and-operators
name: primitive-types-and-operators
category: computing-software
field: software-engineering
product: ocaml
tags: [ocaml, numbers-chars-strings, ocaml-types, int-float-operators, float-of-int, string-immutable]
level: intro
status: docs-checked
description: "Use OCaml's separate int/float operators (+ vs +.), explicit conversions, int overflow wraparound, and immutable strings."
sources: ["https://ocaml.org/manual/", "https://ocaml.org/docs", "https://github.com/ocaml/ocaml/tree/trunk/stdlib", "https://github.com/ocaml/ocaml/tree/trunk/manual/src"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Primitive types and operators

```ocaml
1 + 2        1.0 +. 2.0       (* no implicit int/float coercion *)
float_of_int 3   int_of_float 3.7  (* 3, truncation *)
Float.of_int 3  Int.to_string 3  Float.to_string 2.5
7 / 2 = 3    7 mod 2 = 1  (-7) mod 2 = -1   (* mod sign follows dividend *)
max_int  min_int  (* Sys.int_size bits: 63 on 64-bit platforms *)
"a" ^ "b"   'c'   Char.code 'a'   Char.chr 97
```

## Facts
- `int` is `Sys.int_size` bits wide (63 on 64-bit systems) and operations are taken modulo 2^`Sys.int_size`; use `Int64` for bigger values.
- `=` is structural equality, `==` is physical. `<>` and `!=` are their negations.
- `int_of_string "x"` raises `Failure "int_of_string"`; use `int_of_string_opt`.
- `nan <> nan`; use `Float.equal`/`Float.compare` when NaN matters.

## Gotchas
- `1 / 0` raises `Division_by_zero`; float division by zero gives `infinity`/`neg_infinity` (or `nan`).
- `abs min_int = min_int`.

## Self-check
- [ ] `1.5 + 1` is a type error; `1.5 +. 1.` is fine.

## Checked
2026-11-02. Confirmed: Sys.int_size and modular arithmetic, `abs min_int`, `mod` sign, Division_by_zero, float infinities, int_of_string_opt (stdlib.mli). Removed: Zarith, string/Bytes and short-circuit remarks.
Method: documentation only (OCaml stdlib .mli files and manual .etex sources from github.com/ocaml/ocaml, trunk); no commands were run.
