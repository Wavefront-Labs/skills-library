---
id: computing-software.software-engineering.ocaml.numerics-with-zarith-and-bigarray
name: numerics-with-zarith-and-bigarray
category: computing-software
field: software-engineering
product: ocaml
tags: [ocaml, numerics-zarith, zarith, int64, bigarray, arbitrary-precision]
level: advanced
status: docs-checked
description: "Use Zarith (modules Z and Q) for arbitrary-precision integers and rationals; its GMP requirement and small-int fast path."
sources: ["https://github.com/ocaml/Zarith", "https://raw.githubusercontent.com/ocaml/Zarith/master/z.mli"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Numerics with Zarith

```ocaml
(* libraries: zarith *)
let big = Z.pow (Z.of_int 2) 100
let () = print_endline (Z.to_string big)       (* 1267650600228229401496703205376 *)
```

## Notes
- The module is named `Z`; its interface is similar to `Int32`, `Int64` and `Nativeint` with extra functions. `Q` provides rationals on top of `Z`. `Z.pow : t -> int -> t` raises a base to an `int` exponent.
- The implementation uses GMP (or MPIR). Small integers are represented as unboxed OCaml integers with a faster path that avoids calling GMP; big integers are allocated in the OCaml heap.
- Arbitrary-precision integers can be compared correctly with OCaml's polymorphic comparison operators (`=`, `<`, `>`).
- Requirements: OCaml 4.04.0 or later, GMP or MPIR with development files, and a gcc-compatible C compiler. With findlib use `-package zarith`.
- `Big_int_Z` is a compatibility layer with the API of the legacy `Num` library's Big_int. Support for js_of_ocaml comes from `Zarith_stubs_js`.
- Licence: GNU LGPL v2 with an exception allowing unconstrained static linking.

## Self-check
- [ ] 2^100 prints as 1267650600228229401496703205376.

## Checked

2026-11-08. Read in full: Zarith README; z.mli checked by search for of_int, pow, to_string only (partial read).
Removed: Bigarray, Float and Int64 boxing claims, owl/lacaml, float-printing tip, and the Q expression example (q.mli not read).
Method: documentation only; no commands were run.
