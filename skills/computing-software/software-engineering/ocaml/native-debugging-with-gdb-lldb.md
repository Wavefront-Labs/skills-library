---
id: computing-software.software-engineering.ocaml.native-debugging-with-gdb-lldb
name: native-debugging-with-gdb-lldb
category: computing-software
field: software-engineering
product: ocaml
tags: [ocaml, native-debugging, gdb, lldb, valgrind]
level: advanced
status: draft
description: "Debug ocamlopt binaries with gdb/lldb using -g, find symbols like camlModule__fn, and use perf or valgrind for crashes in C stubs."
sources: ["https://ocaml.org/manual/", "https://ocaml.org/docs"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Native debugging

```bash
dune build ./bin/main.exe                       # dev profile has -g
gdb --args _build/default/bin/main.exe arg
(gdb) break camlDune__exe__Main__fib_123        # symbols are camlModule__name_<stamp>
(gdb) info functions caml_main    (gdb) bt
valgrind --leak-check=full ./main.exe           # mostly for C stubs / FFI
```

## Notes
- Symbol names look like `camlDune__exe__Main__fib_273`; use `info functions fib` to find them. Breakpoint by file:line also works with DWARF info.
- OCaml values are tagged/boxed words; gdb shows raw machine words. The OCaml compiler emits DWARF line info, not type info.
- Segfaults in pure OCaml signal `Obj.magic`, `-unsafe`, `Bytes.unsafe_*`, or a C stub bug.
- `OCAMLRUNPARAM=b` first; `ulimit -c unlimited` for core dumps.
- Address sanitizers: build C stubs with `-fsanitize=address` flags in `foreign_stubs`.

## Self-check
- [ ] A breakpoint on an OCaml function name stops there.
