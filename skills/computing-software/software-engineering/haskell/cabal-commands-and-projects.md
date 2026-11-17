---
id: computing-software.software-engineering.haskell.cabal-commands-and-projects
name: cabal-commands-and-projects
category: computing-software
field: software-engineering
product: haskell
tags: [haskell, cabal-install, cabal-build, cabal-run, cabal-test, cabal-project, cabal-repl, cabal-freeze, v2-commands, cabal-update, cabal-commands-and-projects]
level: practitioner
status: docs-checked
description: "Use cabal v2 commands: update, build, run, test, repl, install, cabal.project with multiple packages and constraints, and freeze files."
sources: ["https://cabal.readthedocs.io/en/stable/cabal-commands.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# cabal commands and cabal.project

**Goal:** the daily cabal-install workflow (v2 "nix-style" commands are the default).

```bash
cabal update                       # refresh the Hackage index
cabal build                        # builds package in the cwd (or all in a project)
cabal build all --enable-tests
cabal run myapp -- --flag arg      # arguments after --
cabal test --test-show-details=direct
cabal repl                         # GHCi with the package loaded; cabal repl myapp:test:myapp-test
cabal bench; cabal haddock; cabal sdist; cabal check
cabal install exe:hlint --overwrite-policy=always    # install an executable to ~/.cabal/bin (or XDG path)
cabal list-bin myapp               # print the path to the built binary
cabal outdated; cabal freeze       # write cabal.project.freeze with exact versions
cabal build --with-compiler=ghc-9.x.y -w ghc-9.x.y
```

## cabal.project
```
packages: ./. ./other-package
tests: True
constraints: aeson ==2.2.*, text >=2.0
allow-newer: foo:base
package myapp
  ghc-options: -Wall
source-repository-package
  type: git
  location: https://example.com/repo.git
  tag: <commit-sha>
index-state: 2026-10-01T00:00:00Z     -- freeze the Hackage view for reproducible solves
```

## Gotchas
- Builds are cached in `dist-newstyle/`; delete it for a clean build.
- `cabal install lib` no longer installs libraries globally; add them to `build-depends` or use `cabal install --lib` with an environment file (discouraged).
- `cabal run` with multiple executables needs the name.
- Commit `cabal.project.freeze` for applications, not libraries.
- `allow-newer` hides real incompatibilities; scope it per package.
- Windows: path length limits can break `dist-newstyle`; enable long paths or build near the drive root.

## Self-check
- [ ] `cabal build all` succeeds from a clean checkout.
- [ ] `index-state` or a freeze file pins reproducible builds.

## Checked

2026-11-02. Confirmed against the Cabal commands page: list-bin, check, outdated, freeze, install --lib, overwrite-policy, freeze file advice. Removed or fixed: none.
Method: documentation only; no commands were run.
