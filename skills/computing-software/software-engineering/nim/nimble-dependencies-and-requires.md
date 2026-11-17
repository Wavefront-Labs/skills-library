---
id: computing-software.software-engineering.nim.nimble-dependencies-and-requires
name: nimble-dependencies-and-requires
category: computing-software
field: software-engineering
product: nim
tags: [nimble-dependencies-and-requires, nimble-package-file, nimble-install, requires, dependencies, version-range, git-dependency, nimble-update, nimble-list, nim]
level: practitioner
status: docs-checked
description: "Declare dependencies with version operators and git URLs in a .nimble file, then install, list, search and refresh packages."
sources:
  - https://nim-lang.github.io/nimble/create-packages.html
  - https://nim-lang.github.io/nimble/use-packages.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dependencies and version requirements

Goal: manage dependencies.

- In the `.nimble` file: `requires "nim >= 2.0.0"`, `requires "fizzbuzz == 1.0"`, `requires "https://github.com/user/pkg#5a54b5e"`, `requires "https://github.com/user/pkg >= 2.0.0"`, `requires "foobar#head"`.
- Operators: `==`, `>`, `<`, `>=`, `<=`, `^=` (latest compatible per semver: `jester ^= 0.4.1` means `>= 0.4.1 & < 0.5.0`) and `~=` (raise the last given digit: `nim ~= 1.2.2` means `>= 1.2.2 & < 1.3.0`; `jester ~= 0.4` means `>= 0.4.0 & < 1.0.0`).
- Git/Mercurial versions come from repository tags that look like versions (e.g. `v0.1`); with no tags Nimble installs HEAD; `#head` forces HEAD.
- Platform-specific dependencies use `when`: `when defined(windows): requires "puppy 1.5.4"`.
- Development-only dependencies: a `dev:` block (alias of `feature "dev"`) with `requires "unittest2"`; feature blocks need the experimental declarative parser (`--parser:declarative`, nimble 0.18.0 and later).
- Install: `nimble install nake`, `nimble install nimgame@0.5`, `nimble install nimgame@"> 0.5"`, `nimble install nimgame@#head`; from a URL `nimble install https://github.com/nimble-test/multi?subdir=alpha`.
- Inside a package directory, `nimble install --depsOnly` installs only the dependencies listed in the package file, globally.
- Maintenance: `nimble refresh` updates the package list (it picks no versions and installs nothing), `nimble list -i` lists installed packages, `nimble search math`, `nimble uninstall nimgame@0.5`, `nimble path itertools` prints installed paths.
- Packages live under `~/.nimble/pkgs2/<name>-<version>-<hash>`. Published names are mapped to URLs in `packages.json` in the official packages repository.

Gotchas:
- `nimble upgrade` is a deprecated alias of `lock --refresh`; it still works but prints a warning.
- Without tags, Nimble installs HEAD, which changes underneath you; pin with `#tag` or a commit.

Verify: `nimble install --depsOnly` in the package directory succeeds.

## Checked

2026-11-08. Read in full: the Nimble User Guide pages "Creating Nimble packages" (dependencies, operators, features, nimble install) and "Use existing Nimble packages" (install forms, list, search, uninstall, refresh, path). Removed: `taskRequires`, the "always require nim with a lower bound" gotcha (the guide shows it only as an example), and the nim-lang/packages registry name (page says "official packages repository" with `packages.json`); manual, tutorial and lib.html dropped from sources.
Method: documentation only; no commands were run.
