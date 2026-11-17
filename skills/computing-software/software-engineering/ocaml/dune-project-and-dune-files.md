---
id: computing-software.software-engineering.ocaml.dune-project-and-dune-files
name: dune-project-and-dune-files
category: computing-software
field: software-engineering
product: ocaml
tags: [ocaml, dune-project-layout, ocaml-dune, dune-project, dune-library, dune-executable, dune-init]
level: practitioner
status: docs-checked
description: "Lay out a dune project: dune-project with lang and generate_opam_files, executable and library stanzas, modules, public_name."
sources: ["https://dune.readthedocs.io/en/stable/reference/dune-project/index.html", "https://dune.readthedocs.io/en/stable/reference/dune-project/generate_opam_files.html", "https://dune.readthedocs.io/en/stable/reference/dune-project/package.html", "https://dune.readthedocs.io/en/stable/reference/dune/library.html", "https://dune.readthedocs.io/en/stable/reference/dune/executable.html", "https://dune.readthedocs.io/en/stable/quick-start.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dune project layout

```bash
dune build                        # no targets: builds the default alias
dune exec -- ./bin/main.exe       # build and run in one step
```
```lisp
; dune-project
(lang dune 3.16)
(name hello)
(generate_opam_files true)
(package (name hello) (depends (ocaml (>= 4.14)) dune))
; bin/dune
(executable (name main) (public_name hello) (libraries hello_lib))
; lib/dune
(library (name hello_lib) (libraries str) (modules :standard))
```

## Notes
- The first line of `dune-project` must be the `lang` stanza, with no extra whitespace or comments; it controls the names and contents of all configuration files dune reads. Use a version your installed dune supports.
- `generate_opam_files` makes dune generate `.opam` files from `dune-project` metadata; build the `@opam` alias to refresh them (`@install` and `@runtest` depend on it). For `(lang dune 3.23)` or newer, changes to checked-in `.opam` files are reported as promotions applied with `dune promote`; with older versions they are promoted automatically. Use `<package-name>.opam.template` for fields dune-project cannot express.
- `package` needs a `name`; `depends` takes names with optional filters or version constraints.
- `executable`: `(name main)` is the module with the entry point and dune can build `main.exe`; `(public_name x)` installs it under that name (`-` means not installed); `(libraries ...)` lists dependencies; `(modules ...)` restricts which modules are used.
- `library`: `name` is required and fixes archive and module names; modules default to all `.ml` files in the directory; without `public_name` it is not installed; `wrapped` defaults to true and the docs recommend keeping it (so module `Foo` in library `mylib` is `Mylib.Foo`).

## Self-check
- [ ] `dune build && dune exec -- ./bin/main.exe` prints your program output.

## Checked
Checked 2026-11-08 against the dune-project, generate_opam_files, package, library, executable and quick-start pages. Removed: `dune init project` and its generated layout, `dune exec hello` by public name, `@check`/`@all` description, the `_build` gitignore tip and the `dune --version` advice, none of which those pages state. Unchanged: stanza semantics above; the sample files were not built.

Method: documentation only; no commands were run.
