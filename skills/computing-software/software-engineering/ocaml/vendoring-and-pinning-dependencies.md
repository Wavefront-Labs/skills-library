---
id: computing-software.software-engineering.ocaml.vendoring-and-pinning-dependencies
name: vendoring-and-pinning-dependencies
category: computing-software
field: software-engineering
product: ocaml
tags: [ocaml, dune-vendoring, vendored-dirs, dune-workspace, opam-monorepo, local-fork]
level: advanced
status: docs-checked
description: "Vendor source trees with (vendored_dirs), use dune-workspace contexts, and pin local forks of dependencies with opam."
sources: ["https://dune.readthedocs.io/", "https://github.com/ocaml/dune/blob/main/doc/reference/dune/vendored_dirs.rst", "https://github.com/ocaml/dune/blob/main/doc/reference/dune-workspace/context.rst", "https://github.com/ocaml/dune/blob/main/doc/reference/dune-workspace/profile.rst", "https://opam.ocaml.org/doc/Manual.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Vendoring and workspaces

```lisp
; dune at repo root
(vendored_dirs vendor)
; dune-workspace
(lang dune 3.16)
(context default)
(context (default (name release) (profile release)))
```

## Notes
- `vendored_dirs` (since Dune 1.11) marks directories holding vendored Dune projects. Dune does not resolve aliases there, so by default it does not build all installable targets, run tests, format or lint that code, while still building your dependencies. Libraries and executables there are built with `-w -a`, suppressing all warnings.
- A `dune-workspace` can declare several `(context ...)` stanzas, each building the same sources with a different configuration into its own `_build/<name>` directory (default context name is `default`). `(context (default (name N) (profile P)))` sets the profile; a context profile takes precedence over `--profile`.
- Contexts can also be `(opam (switch <name>))`, and `(toolchain <findlib_toolchain>)`, `(host ...)` and `(targets ...)` support cross compilation.
- Merlin reads artefacts of a single context (normally `default`); add `(merlin)` to another context to change that.
- For a local fork, use opam pinning: `opam pin [package] <URL>` can divert a package's source to a local path with a development or patched version, and `opam install <DIR>` pins packages defined in a directory. Pins are local to the current switch.
- Dune's own package management has a `(pin ...)` stanza (since 3.14) but its docs state the feature is not final.

## Self-check
- [ ] Vendored code builds in the same `dune build` invocation as the main code.

## Checked
Date: 2026-11-08. Confirmed against Dune docs source on GitHub: reference/dune/vendored_dirs.rst, reference/dune-workspace/context.rst, reference/dune-workspace/profile.rst, reference/dune-project/pin.rst, and the opam manual section on pinning. Removed: the opam-monorepo/duniverse paragraph (not covered by the pages read) and the claim that vendored code is excluded from `@all` by that name.
Method: documentation only; no commands were run.
