---
id: computing-software.software-engineering.fortran.fpm-project
name: fpm-project
category: computing-software
field: software-engineering
product: fortran
tags: [fortran, fpm-project, fortran-fpm]
level: intro
status: docs-checked
description: "Create an fpm project with fpm new, run it and its tests, and know the default layout and the ways to install fpm."
sources:
  - https://fpm.fortran-lang.org/tutorial/hello-fpm.html
  - https://fpm.fortran-lang.org/install/index.html
  - https://fpm.fortran-lang.org/spec/manifest.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Creating and running projects with fpm
**Goal:** start a project with fpm.
```bash
fpm new first_steps
cd first_steps
fpm run
fpm test
```
- `fpm new` creates a git repository with a dummy project in the standard layout: `app/main.f90` (executable), `src/<name>.f90` (library module), `test/check.f90`, `fpm.toml` and `README.md`. Examples live in `example/` and are discovered like `app` and `test` (manifest reference).
- `fpm run` builds and runs the executable; the generated program prints a hello line. `fpm test` runs the test stub, which prints "Put some tests in here!".
- fpm tracks changes in the project automatically when you use `run` and `test`.
- The generated `fpm.toml` sets `auto-executables`, `auto-tests` and `auto-examples` to true and `[install] library = false`; see the fpm-manifest skill for the keys.
- Installing fpm (install page): release binaries for macOS, Linux and Windows (x86-64; checksums are published as `.sha256` files), Homebrew via the `fortran-lang/homebrew-fortran` tap, `pipx install fpm` from PyPI, or conda-forge.
## Gotchas
- With no `[[executable]]` section, fpm discovers programs in `app`; an explicit executable must set `name`.
- Run flags and options (build profile, extra compiler flags, install prefix) are in fpm's command-line reference, which was not read for this check; look them up there rather than guessing.
## Self-check
`fpm run` in a fresh project prints "Hello, first_steps!" (the project name appears in the message).

## Checked
Checked against the fpm "First steps with fpm" tutorial, the install page and the manifest reference.
Removed: the `fpm new --app --test/--lib/--bare`, `fpm build`, `--profile release`, `--flag`, `--verbose` and `fpm install --prefix` claims (the CLI reference page was unavailable), the claim that fpm is written in Fortran, and the unique-module-names gotcha.
Method: docs-only read of cited pages, 2026-11-08
