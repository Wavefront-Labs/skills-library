---
id: computing-software.software-engineering.ada.alire-crate-management
name: alire-crate-management
category: computing-software
field: software-engineering
product: ada
tags: [ada, alire-crate-management, gnat-alire]
level: practitioner
status: docs-checked
description: "Use alr: init, with, build, run, search, update, toolchain selection, and the alire.toml manifest for Ada/SPARK crates."
sources:
  - https://alire.ada.dev/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Alire: create, build and manage crates
```
alr init --bin my_app          # new executable crate
cd my_app; alr with gnatcoll   # add dependency
alr build; alr run
alr search --crates json; alr update
```
- `alire.toml` holds name, version, description, licenses, maintainers and `[[depends-on]]` dependencies.
- `alr init --lib` makes a library crate; `--in-place` uses the current directory; `--no-skel` keeps an existing GPR file.
- `alr with --del crate` removes a dependency; `alr with` alone lists them (`--tree`, `--solve` for detail).
- `alr search --list` shows the latest release of every crate.
- `alr toolchain --select` picks the preferred GNAT compiler; plain `alr toolchain` shows what is installed.
## Gotchas
- The project file must still set `Target` for a cross compiler; Alire only looks at `depends-on`.
## Self-check
Create a crate, add a dependency, build and run.

## Checked
2026-11-03. Confirmed in the Alire documentation (alire.ada.dev/docs): `alr init --bin/--lib/--in-place/--no-skel`, `alr with`, `alr build`, `alr run`, `alr search`, `alr update`, `alr toolchain --select`, manifest properties. Removed `alr pin`, build-profile flags and the toolchain download/offline gotcha (not on the pages read).
Method: documentation only; no commands were run.
