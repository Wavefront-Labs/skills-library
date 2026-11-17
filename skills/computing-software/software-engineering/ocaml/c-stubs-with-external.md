---
id: computing-software.software-engineering.ocaml.c-stubs-with-external
name: c-stubs-with-external
category: computing-software
field: software-engineering
product: ocaml
tags: [ocaml, c-stubs, ocaml-ffi, external-declaration, camlparam, foreign-stubs]
level: advanced
status: docs-checked
description: "Bind C functions with external, write stubs using CAMLparam/CAMLlocal/CAMLreturn, and use [@@noalloc], [@unboxed] and [@untagged]."
sources: ["https://ocaml.org/manual/", "https://ocaml.org/docs"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# C stubs

```ocaml
external add : int -> int -> int = "caml_add_stub"          (* simple: values are tagged ints *)
external fast : (float [@unboxed]) -> (float [@unboxed]) = "stub_byte" "stub_native" [@@noalloc]
```
```c
#include <caml/mlvalues.h>
#include <caml/memory.h>
#include <caml/alloc.h>
value caml_add_stub(value a, value b) { return Val_long(Long_val(a) + Long_val(b)); }
value stub_str(value s) { CAMLparam1(s); CAMLlocal1(r); r = caml_copy_string("hi"); CAMLreturn(r); }
```

## Notes
- Values that may hold heap pointers must be registered with `CAMLparam`/`CAMLlocal` whenever a GC can happen (allocation, `caml_callback`). `CAMLreturn` is required if you used CAMLparam.
- Ints: `Val_long`/`Long_val`; strings: `String_val`, `caml_string_length`; options and variants are blocks with tags.
- Bytecode needs two stubs when arguments exceed five (`stub_byte` takes `value *argv, int argn`).
- `[@@noalloc]` avoids the indirection of a normal external call, but only if the C function does not allocate, does not raise exceptions and does not release the domain lock; `[@untagged]` and `[@unboxed]` pass untagged integers and unboxed floats.
- To release the domain lock around a long or blocking C call use `caml_release_runtime_system()` and `caml_acquire_runtime_system()` (from `<caml/threads.h>`); no OCaml data may be accessed in between.
- Raise exceptions with `caml_failwith`, `caml_invalid_argument`.

## Self-check
- [ ] A GC-stress run (`OCAMLRUNPARAM=s=4k`) still returns correct results.

## Checked

2026-11-03. Confirmed against the OCaml 5.5 manual: the C interface chapter (Val_long/Long_val, String_val, caml_string_length, caml_copy_string, CAMLparam/CAMLlocal/CAMLreturn, bytecode primitives with more than 5 arguments, [@@noalloc], [@unboxed], [@untagged], caml_failwith, caml_invalid_argument, release/acquire of the runtime system) and the ocamlrun page (OCAMLRUNPARAM s=4k).

Removed or corrected: the dune foreign_stubs stanza (dune is not in the manual) and the caml_enter_blocking_section wording (the manual documents the release/acquire pair).

Method: documentation only; no commands were run.
