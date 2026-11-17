---
id: computing-software.software-engineering.ocaml.using-compiler-libs-and-ocamlobjinfo
name: using-compiler-libs-and-ocamlobjinfo
category: computing-software
field: software-engineering
product: ocaml
tags: [ocaml, compiler-libs, ocamlobjinfo, cmt-files, typedtree]
level: advanced
status: draft
description: "Inspect .cmi/.cmt/.cmx with ocamlobjinfo and read Typedtree via compiler-libs for tooling; know API instability."
sources: ["https://ocaml.org/manual/", "https://ocaml.org/docs"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# compiler-libs and object info

```bash
ocamlobjinfo _build/default/lib/.mylib.objs/byte/mylib.cmi      # interface and imports
ocamlobjinfo foo.cmxa
ocamlfind ocamlc -package compiler-libs.common -linkpkg tool.ml
```
```ocaml
(* libraries: compiler-libs.common *)
let () = Printf.printf "%s\n" Config.version
```

## Notes
- `compiler-libs` exposes the compiler's own modules (`Parsetree`, `Typedtree`, `Env`); its API changes with every compiler release, so tools pin an OCaml version or use `ppxlib`'s stable AST.
- `.cmt` (typed tree) files from `-bin-annot` power Merlin, odoc and `ocaml-index`.
- `ocamlobjinfo` lists unit names, CRCs and dependencies: useful for "inconsistent assumptions over interface" errors.
- "Inconsistent assumptions over interface X" means two units were compiled against different `.cmi` versions of X: clean and rebuild (`dune clean`).

## Self-check
- [ ] `ocamlobjinfo` prints the imported interfaces of a compiled unit.
