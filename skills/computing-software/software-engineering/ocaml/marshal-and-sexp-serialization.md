---
id: computing-software.software-engineering.ocaml.marshal-and-sexp-serialization
name: marshal-and-sexp-serialization
category: computing-software
field: software-engineering
product: ocaml
tags: [ocaml, marshal-sexp, marshal-module, sexp, ppx-sexp-conv]
level: advanced
status: docs-checked
description: "Serialize OCaml values with Marshal: its flags, lack of type safety, and why untrusted data must never be unmarshalled."
sources: ["https://ocaml.org/docs", "https://erratique.ch/software/cmdliner"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Marshal

```ocaml
let s = Marshal.to_string (1, "a") []
let (n, str) : int * string = Marshal.from_string s 0     (* type NOT checked *)
```

## Notes
- `Marshal.from_*` is not type-safe: the type of the data is not transmitted, so give the expected type explicitly. Never unmarshal untrusted data.
- The byte format is compatible across machines for a given OCaml version; `Marshal.Compat_32` makes a 64-bit writer fail on integers a 32-bit reader cannot represent.
- Functional values need the `Marshal.Closures` flag and can only be read back by exactly the same program.
- Unmarshalled extensible variants such as exceptions must not be pattern-matched, and channels used with `Marshal.to_channel`/`from_channel` must be opened in binary mode.

## Self-check
- [ ] No Marshal.from_* on network or user-supplied files.

## Checked

2026-11-03. Confirmed against the OCaml 5.5 manual: the Marshal API page (not type-safe warning, to_string/from_string, Closures, Compat_32, same-version compatibility, extensible variants, binary-mode channels).

Removed or corrected: all sexplib, ppx_sexp_conv, ocaml-protoc and bin_prot content (not covered by the manual), and the unsourced segfault and code-execution claims.

Method: documentation only; no commands were run.
