---
id: computing-software.software-engineering.ocaml.dune-ppx-flags-and-profiles
name: dune-ppx-flags-and-profiles
category: computing-software
field: software-engineering
product: ocaml
tags: [ocaml, dune-ppx-preprocess, dune-preprocess, dune-env, dune-flags, ppx-dune]
level: advanced
status: docs-checked
description: "Add ppx via (preprocess (pps ...)), set (flags) and (ocamlopt_flags), and use env stanzas and build profiles."
sources: ["https://dune.readthedocs.io/", "https://github.com/ocaml/dune/blob/main/doc/reference/preprocessing-spec.rst", "https://github.com/ocaml/dune/blob/main/doc/reference/dune/env.rst", "https://github.com/ocaml/dune/blob/main/doc/reference/dune-workspace/profile.rst", "https://github.com/ocaml/dune/blob/main/doc/concepts/ocaml-flags.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dune preprocessing and flags

```lisp
(library
 (name mylib)
 (libraries base)
 (preprocess (pps ppx_deriving.show ppx_deriving.eq))
 (flags (:standard <extra flags>))
 (ocamlopt_flags (:standard <extra flags>)))
```
```lisp
; dune (at root)
(env
 (dev (flags (:standard <extra flags>)))
 (release (ocamlopt_flags (:standard <extra flags>))))
```

## Notes
- Flag fields are `flags` (shared by `ocamlc` and `ocamlopt`), `ocamlc_flags` and `ocamlopt_flags`; the last two are appended to `flags`. They work in `library`, `executable`, `executables` and `env`.
- Write `(flags (:standard ...))`: the default is taken from the environment, and omitting `:standard` replaces the defaults (for example `(ocamlopt_flags ())` removes the default `-g`).
- With `(lang dune 3.21)` or later: all profiles add `-g` to `ocamlc_flags` and `ocamlopt_flags`; `dev` adds `-short-paths -keep-locs -warn-error +a` to `flags`; `release` and user-defined profiles add no common flags; no profile adds `-O2` or `-O3`.
- `env` stanzas hold per-profile settings: the first `(<profile> <settings>)` form matching the selected profile is used, and `_` matches any profile. Profiles need no declaration; any name can be passed to `--profile` or set in `dune-workspace`.
- Standard profiles are `dev` (default; warnings-as-errors, `-opaque`, `%{inline_tests}` enabled) and `release` (used for opam releases and `dune build -p <package>`; no warnings-as-errors, inline tests disabled).
- `(preprocess (pps ...))` uses the fast pipeline; `(staged_pps ...)` uses the classic `-ppx` pipeline. Arguments starting with `-` are flags, and `--` separates flags that do not start with `-`: `(pps ppx1 -foo ppx2 -- -bar 42)`.
- A ppx rewriter library with runtime dependencies declares them in `(ppx_runtime_libraries (...))`.
- `(preprocessor_deps ...)` declares extra dependencies of a preprocessor; `(lint (pps ...))` runs the ppx driver in lint mode under `dune build @lint`, with corrections applied by `dune promote`.
- `(inline_tests)` in a library enables inline tests.

## Self-check
- [ ] `dune build` passes with the default profile and with `--profile release`.

## Checked
Date: 2026-11-08. Confirmed against Dune docs source on GitHub: preprocessing-spec.rst, dune/env.rst, dune/library.rst (preprocess, lint, preprocessor_deps, ppx_runtime_libraries, inline_tests), dune-workspace/profile.rst and concepts/ocaml-flags.rst. Removed: specific warning numbers, the claim that -O3 only matters on flambda switches, the `--release` flag (use `--profile release`), the cookie example, `let%test` details, and the advice on warnings 32/33.
Method: documentation only; no commands were run.
