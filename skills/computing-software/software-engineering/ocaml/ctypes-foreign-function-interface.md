---
id: computing-software.software-engineering.ocaml.ctypes-foreign-function-interface
name: ctypes-foreign-function-interface
category: computing-software
field: software-engineering
product: ocaml
tags: [ocaml, ctypes, libffi, foreign-function, c-bindings]
level: advanced
status: docs-checked
description: "Bind C libraries from OCaml with ctypes: foreign, @-> returning, structures with field and seal, allocate, Cstubs."
sources: ["https://github.com/yallop/ocaml-ctypes", "https://raw.githubusercontent.com/yallop/ocaml-ctypes/master/src/ctypes/ctypes.mli"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ctypes

```lisp
(executable (name main) (libraries ctypes ctypes.foreign))
```
```ocaml
open Ctypes
open Foreign
let abs_c = foreign "abs" (int @-> returning int)
let () = Printf.printf "%d\n" (abs_c (-3))
```

## Notes
- ctypes binds C libraries in pure OCaml: combinators describe C types (numeric types, arrays, pointers, structs, unions, functions) and you bind functions directly, with no C stubs written or generated.
- `foreign : string -> ('a -> 'b) fn -> ('a -> 'b) result` is part of the FOREIGN interface; the `Foreign` and `Cstubs` modules are its two implementations. Use `Cstubs` when you want generated stubs; `Cstubs_structs` determines struct layout reliably.
- Structures: `structure "t"`, then `field t "x" int`, then `seal t`.
- `allocate ?finalise typ v` allocates a fresh value, initialises it with `v` and returns its address; the value is freed automatically once no references to the pointer remain, and `finalise` runs just before. `!@` dereferences a pointer; `CArray` is the array module.
- `coerce` / `coerce_fn` support is subject to change between versions.
- Further reading from the README: the ctypes tutorial and FAQ wiki pages and Real World OCaml chapter on the foreign function interface.

## Self-check
- [ ] The example prints 3.

## Checked

2026-11-08. Read in full: ocaml-ctypes README, and ctypes.mli (allocate, `!@`, CArray, FOREIGN signature, coerce notes) plus the types signature for structure, field and seal.
Removed: libffi runtime and performance claims, Dl.dlopen/`~from`, malloc/finaliser GC claim, callbacks-and-threads and platform-path notes, ocaml.org landing sources.
Method: documentation only; no commands were run.
