---
id: computing-software.software-engineering.ocaml.bytecode-executables-and-custom-runtime
name: bytecode-executables-and-custom-runtime
category: computing-software
field: software-engineering
product: ocaml
tags: [ocaml, bytecode-executables, ocaml-runtime-bytecode, ocamlrun, ocamlc-custom, bytecode-executable, output-complete-exe]
level: advanced
status: gated
description: "Build bytecode with ocamlc, run through ocamlrun, make self-contained executables with -custom or -output-complete-exe, and compare to native."
sources: ["https://ocaml.org/manual/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bytecode executables

```bash
ocamlfind ocamlc -package unix -linkpkg -o prog.byte main.ml
ocamlrun prog.byte           # needs the runtime installed
ocamlfind ocamlc -custom -o prog.custom main.ml          # bundles runtime (needs a C compiler)
ocamlfind ocamlc -output-complete-exe -o prog.exe main.ml
```
```lisp
(executable (name main) (modes byte exe))   ; builds main.bc and main.exe
```

## Notes
- Bytecode is portable across machines with the same OCaml version, slower (roughly several times) than native, and supports ocamldebug.
- `#!/path/to/ocamlrun` header lets a `.byte` file run as a script; dynamic stubs (`dllunix.so`) must be found via `ld.conf`/`CAML_LD_LIBRARY_PATH`.
- `-custom`/`-output-complete-exe` link the runtime for distribution without installing OCaml.
- Dune modes: `byte`, `native`, `exe`, `byte_complete`, `js` (see dune docs for exact names).
- Use bytecode for fast compile cycles in big projects (`dune build @check` is even faster).

## Self-check
- [ ] The `-custom` binary runs on a machine without OCaml installed (same OS/arch).

## Checked

- Date: 2026-11-02.
- Source pages listed in `sources` were fetched where possible; the manual root was fetched but not the runtime/bytecode chapters; flags and file names not checked. Treat the specific names, flags and figures as unconfirmed (gated: unconfirmed, source is paywalled or blocked).

Method: documentation only; no commands were run.
