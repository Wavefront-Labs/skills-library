---
id: computing-software.software-engineering.ocaml.multiple-libraries-and-packages-in-one-repo
name: multiple-libraries-and-packages-in-one-repo
category: computing-software
field: software-engineering
product: ocaml
tags: [ocaml, dune-multi-package, ocaml-workspaces, multi-package, public-name, dune-package, monorepo-libraries]
level: practitioner
status: docs-checked
description: "Split a repo into multiple libraries and opam packages with public_name, package fields and generate_opam_files."
sources: ["https://dune.readthedocs.io/", "https://github.com/ocaml/dune/blob/main/doc/reference/packages.rst", "https://github.com/ocaml/dune/blob/main/doc/reference/dune/library.rst", "https://github.com/ocaml/dune/blob/main/doc/reference/dune-project/package.rst", "https://github.com/ocaml/dune/blob/main/doc/reference/dune-project/generate_opam_files.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Multi-library and multi-package repos

```lisp
; dune-project
(lang dune 3.16)
(generate_opam_files)
(package (name core_lib) (depends ocaml dune))
(package (name cli_tool) (depends core_lib cmdliner))
; core/dune
(library (name core_lib) (public_name core_lib))
; cli/dune
(executable (name main) (public_name cli-tool) (package cli_tool) (libraries core_lib cmdliner))
```

## Notes
- Packages are defined by a `<package-name>.opam` file or by a `(package (name ...))` stanza in `dune-project`. If you are not publishing to opam, prefer the `dune-project` stanza over empty `.opam` files.
- A library without `(public_name)` is not installed by Dune. The public name must start with the package name, optionally followed by a dot and a suffix: `(public_name core_lib.sub)` belongs to package `core_lib`.
- `(package <package>)` on a library installs a private library under that package; public libraries in the same project can use it, but its interface is hidden from consumers outside the project.
- An executable or test with a `(public_name)` is attached to a package by its `(package)` field, which can be omitted when there is only one package.
- Libraries only consume modules from the directory of their stanza; a multi-directory library needs the `include_subdirs` stanza.
- `(generate_opam_files)` in `dune-project` makes Dune generate `<package>.opam` from `(package)` metadata; `dune build @opam` refreshes them. Extra opam fields go in `<package-name>.opam.template`.
- `dune build -p <package>` (or `--only-packages`) limits the build to the given packages; it is also what opam release builds use (release profile).
- A `(dir <path>)` field in `(package)` (since 3.21) gives a package its own directory so that excluding other packages leaves their stanzas out of the build entirely.

## Self-check
- [ ] `dune build -p cli_tool` builds without building unrelated packages.

## Checked
Date: 2026-11-08. Confirmed against Dune docs source on GitHub: reference/packages.rst, reference/dune/library.rst (public_name, package, include_subdirs note), reference/dune-project/package.rst (name, depends, dir, `-p`), reference/dune-project/generate_opam_files.rst and reference/dune-workspace/profile.rst. Removed: the claims that dune reports cyclic dependencies, that directory layout is free, that `-p` builds dependencies of the package, and `(libraries core_lib.sub)` as a rule.
Method: documentation only; no commands were run.
