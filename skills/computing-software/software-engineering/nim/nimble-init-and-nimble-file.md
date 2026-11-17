---
id: computing-software.software-engineering.nim.nimble-init-and-nimble-file
name: nimble-init-and-nimble-file
category: computing-software
field: software-engineering
product: nim
tags: [nimble-init-and-nimble-file, nimble-package-file, nimble, nimble-init, nimble-file, requires, srcdir, bin, version, package-layout, nim]
level: intro
status: docs-checked
description: "Start a package with nimble init and the .nimble fields: required fields, srcDir, bin/namedBin/binDir, backend, install and skip lists, requires, check and dump."
sources:
  - https://github.com/nim-lang/nimble/blob/master/nimble-guide/docs/create-packages.md
  - https://github.com/nim-lang/nimble/blob/master/nimble-guide/docs/nimble-reference.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# nimble init and the .nimble file fields

Goal: define a package.

- `nimble init` run in an empty directory starts a wizard: package type (library, binary or hybrid), initial version (default 0.1.0), description, license (ideally an SPDX identifier) and lowest supported Nim version. For a package `myPackage` it creates `myPackage.nimble`, `src/myPackage.nim`, `src/myPackage/submodule.nim`, `tests/config.nims` and `tests/test1.nim`.
- The generated file looks like:
```nim
version       = "0.1.0"
author        = "username"
description   = "Check if a number is odd."
license       = "MIT"
srcDir        = "src"

requires "nim >= 2.0.0"
```
- Required fields: `version`, `author`, `description`, `license` (`name` is not needed in the NimScript format). Bump `version` before tagging a release.
- Optional fields from the reference: `srcDir` (default: the directory of the .nimble file), `binDir` (where `nimble build` puts binaries), `bin` (files to build, no extension), `namedBin` (`name:value` pairs; overrides duplicates in `bin`), `backend` (`c`, `cc`, `cpp`, `objc`, `js`), `installDirs`, `installFiles`, `installExt` (exclusive install lists), `skipDirs`, `skipFiles`, `skipExt`, `paths`.
- When sources live in `src`, the .nimble file must contain `srcDir = "src"`. Extra modules go in a directory named after the package (`src/foobar/utils.nim` is imported as `foobar/utils`); a `private` directory hides modules from users.
- Dependencies: `requires "nim >= 2.0.0"`, `requires "fizzbuzz == 1.0"`, or a URL such as `requires "https://github.com/user/pkg >= 2.0.0"`. Operators: `==`, `>`, `<`, `>=`, `<=`, `^=` (semver-compatible), `~=`.
- `nimble check` validates the package structure; `nimble dump` prints package metadata (`--json` or `--ini`).

Gotchas:
- `nimble check` errors when source files sit in a directory not named after the package; rename it or add it to `skipDirs`.
- The .nimble file is NimScript, so `when defined(...)` can guard `requires`.

Verify: `nimble check` reports the package is valid.

## Checked

2026-11-03. Confirmed in the Nimble guide pages "Creating Nimble packages" and ".nimble file reference": wizard prompts and generated layout, required/optional fields, backend values, version operators, `check`, `dump`. Removed: claims that the nimble file name must equal the package name, that versions must be "semver-like", and the `cligen >= 1.6` example (not in the pages).
Method: documentation only; no commands were run.
