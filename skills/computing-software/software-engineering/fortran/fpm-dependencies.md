---
id: computing-software.software-engineering.fortran.fpm-dependencies
name: fpm-dependencies
category: computing-software
field: software-engineering
product: fortran
tags: [fortran, fpm-dependencies, fortran-fpm]
level: practitioner
status: docs-checked
description: "Add git, path and registry dependencies, dev-dependencies and target-specific dependencies to fpm.toml, pinned by tag or revision."
sources:
  - https://fpm.fortran-lang.org/spec/manifest.html
  - https://fpm.fortran-lang.org/tutorial/dependencies.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# fpm dependencies
**Goal:** reuse libraries with fpm.
```toml
[dependencies]
stdlib = "*"
toml-f = { git = "https://github.com/toml-f/toml-f", tag = "v0.2.1" }
my-utils = { path = "utils" }
[dev-dependencies]
test-drive.git = "https://github.com/fortran-lang/test-drive"
test-drive.tag = "v0.4.0"
[[executable]]
name = "demo"
[executable.dependencies]
M_CLI2.git = "https://github.com/urbanjost/M_CLI2"
```
- Git dependencies take `git` plus optionally `branch`, `tag` or `rev` (a commit hash). Use `tag` or `rev` to pin a version.
- Path dependencies use `path`, relative to the `fpm.toml` that declares them, with `/` as separator on all platforms.
- Dependencies declared in the manifest root are exported with the project. `dev-dependencies` are available to all tests but not exported; the tutorial pins its test framework (test-drive) by tag.
- Dependencies can also be declared inside a single `[[executable]]` or `[[test]]` (for example a command-line parsing package used only by the executable).
- Registry dependencies need the registry set up first (read the fpm registry instructions) and a namespace: `my-package.namespace = "my-namespace"` fetches the newest version, and `my-package.v = "1.0.0"` selects a version. The tutorial's `stdlib = "*"` form pulls the Fortran standard library.
- Since fpm 0.9.1 a dependency can receive its own preprocessor macros, for example `preprocess.cpp.macros = ["REAL32"]`; fpm does not check them for collisions with the dependency's own manifest.
## Gotchas
- Dependencies declared at the manifest root are exported to anything that depends on your package, so put test-only packages under `dev-dependencies` and tool-only packages under the target.
## Self-check
Add a git dependency, run the project with fpm, and confirm it is fetched and builds.

## Checked
Checked against the fpm manifest reference (dependency sections) and the "Adding dependencies" tutorial.
Removed: the `--profile`, `--flag` and `--verbose` command-line claims (the profiles section and CLI reference were not among the pages read), `test-drive` v0.5.0 (tutorial uses v0.4.0), the "vendor for offline use" advice, and the unique-module-names claim (not on the pages read).
Method: docs-only read of cited pages, 2026-11-08
