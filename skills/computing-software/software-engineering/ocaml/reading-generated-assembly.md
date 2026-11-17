---
id: computing-software.software-engineering.ocaml.reading-generated-assembly
name: reading-generated-assembly
category: computing-software
field: software-engineering
product: ocaml
tags: [ocaml, assembly-output, ocamlopt-asm-output, assembly, allocation-sequence, code-generation]
level: advanced
status: docs-checked
description: "Emit assembly with ocamlopt -S and compare the effect of -unsafe on bounds and division checks."
sources: ["https://ocaml.org/manual/5.5/native.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Assembly output

```bash
ocamlfind ocamlopt -S -c x.ml          # writes x.s
ocamlfind ocamlopt -S -unsafe -c x.ml  # compare: bounds checks off
```

## Notes
- `-S` keeps the assembly produced during compilation; for `x.ml` it is saved as `x.s`.
- `-unsafe` turns off bound checking for array and string accesses (`v.(i)`, `s.[i]`) and the zero-divisor check for integer division and modulus. Out-of-bounds access then has undefined behaviour, and division by zero can halt the program or give an unspecified result instead of raising `Division_by_zero`.
- Diffing the `.s` files with and without `-unsafe` shows which checks were removed.

## Self-check
- [ ] The `.s` file with `-unsafe` has fewer bounds-check branches than the one without.

## Checked
Date: 2026-11-08. Confirmed against the OCaml 5.5 manual ocamlopt page (option entries for -S and -unsafe read; page not read in full). Removed: symbol naming, the r15 allocation pointer, `caml_call_gc`, float unboxing, `caml_compare` and `objdump` claims (no manual source), plus the ocaml.org/manual and ocaml.org/docs landing sources.
Method: documentation only; no commands were run.
