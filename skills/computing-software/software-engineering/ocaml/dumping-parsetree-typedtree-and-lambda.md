---
id: computing-software.software-engineering.ocaml.dumping-parsetree-typedtree-and-lambda
name: dumping-parsetree-typedtree-and-lambda
category: computing-software
field: software-engineering
product: ocaml
tags: [ocaml, dump-source-lambda, ocaml-compiler-inspection, dsource, dparsetree, dlambda, compiler-stages]
level: advanced
status: draft
description: "Inspect each compiler stage with -dsource/-dparsetree/-dtypedtree/-dlambda and read pattern-match compilation and desugaring."
sources: ["https://ocaml.org/manual/", "https://ocaml.org/docs"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Compiler stage dumps

```bash
ocamlfind ocamlopt -dsource -c x.ml        # pretty-printed source after ppx
ocamlfind ocamlopt -dparsetree -c x.ml
ocamlfind ocamlopt -dtypedtree -c x.ml
ocamlfind ocamlopt -dlambda -c x.ml        # lambda IR; shows match compilation
ocamlfind ocamlopt -dcmm -c x.ml           # C-- IR
```

## Notes
- `-dsource` after ppx is the quick way to see what a deriver generated; `dune describe pp x.ml` does it through dune.
- `-dlambda` shows if pattern matches became jumptables or comparisons, and whether closures/allocations are present.
- With flambda: `-dflambda` and `-dflambda-verbose`.
- Use dune `(ocamlopt_flags (:standard -dlambda))` and read `_build/log`.
- Output formats vary by compiler version.

## Self-check
- [ ] You can locate the generated function from a deriver in the `-dsource` output.
