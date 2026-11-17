---
id: computing-software.software-engineering.fortran.fpm-manifest
name: fpm-manifest
category: computing-software
field: software-engineering
product: fortran
tags: [fortran, fpm-manifest, fortran-fpm]
level: practitioner
status: docs-checked
description: "Write fpm.toml: package metadata, build auto-discovery, library, executable and test targets, [fortran] settings, install and preprocess tables."
sources:
  - https://fpm.fortran-lang.org/spec/manifest.html
  - https://fpm.fortran-lang.org/tutorial/hello-fpm.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# fpm.toml manifest
**Goal:** configure fpm builds. Checked against the fpm manifest reference (which documents features up to fpm v0.13.0); use the reference for your installed version.
```toml
name = "myproj"
version = "0.1.0"
license = "MIT"
[build]
auto-executables = true
auto-tests = true
auto-examples = true
[install]
library = true
[[executable]]
name = "myapp"
source-dir = "app"
main = "main.f90"
```
- Only `name` is required; the project name is the default name of the library and executable targets. `version` is a string following Semantic Versioning, or a filename relative to the project root that holds the version. `license` takes an SPDX identifier (for example `Apache-2.0 OR MIT`).
- `[library]`: the library is built if the source or include directory exists; defaults are `src` and `include`, changed with `source-dir` and `include-dir`. Since v0.12.0 `type` selects `monolithic` (default), `static` or `shared`; since v0.13.0 an array such as `["shared", "static"]` builds several, but `monolithic` cannot be combined with others.
- Executables, examples and tests: with no `[[executable]]`, `[[example]]` or `[[test]]` section fpm searches the `app`, `example` and `test` directories for programs. An explicit section must set `name`; `source-dir` and `main` are optional. `auto-executables`, `auto-examples` and `auto-tests` (default on) toggle discovery.
- `[fortran]`: `implicit-typing` and `implicit-external` (both default false) and `source-form` (`"free"` default, `"fixed"`, or `"default"` to let the compiler decide).
- `[build]` `link` names external libraries; order matters, so a library must appear before the libraries it depends on (`["lapack", "blas"]`). `external-modules` lists modules outside the package, and fpm cannot locate their `.mod` files itself: pass include directories through compiler flags.
- `[install]`: by default only executables are installed; `library = true` also installs module files and the archive. `module-dir` (since v0.13.0) sets where `.mod` files go, relative to the prefix, otherwise `include/`.
- `[preprocess.cpp]` takes `suffixes`, `directories` and `macros` (for example `macros = ["FOO=2"]`); `fypp` is also accepted as a preprocessor name. Since v0.13.0 fpm evaluates CPP conditionals against manifest macros when resolving module dependencies; the compiler still does the actual preprocessing.
- `[extra]` is free data for third-party tools and is never evaluated by fpm; use subtables named after the tool.
## Gotchas
- Manifest keys have grown across releases (library `type` needs v0.12.0, `module-dir` and CPP parsing need v0.13.0); check the reference against your installed version.
- Running `fpm new <name>` produces a manifest with `auto-executables`, `auto-tests` and `auto-examples` set to true and `[install] library = false`.
## Self-check
Run the build for the project and confirm the targets you declared are the ones built.

## Checked
Checked against the fpm manifest reference and the "First steps with fpm" tutorial (full text).
Removed: the claim that `[extra]`, `[[test]]`, `[[example]]` "follow the executable pattern" beyond what the reference states, hedged "confirm keys" notes now replaced by the documented keys, and the `fpm build --verbose` self-check (flag not documented in the pages read).
Method: docs-only read of cited pages, 2026-11-08
