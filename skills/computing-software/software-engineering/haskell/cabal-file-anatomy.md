---
id: computing-software.software-engineering.haskell.cabal-file-anatomy
name: cabal-file-anatomy
category: computing-software
field: software-engineering
product: haskell
tags: [haskell, cabal-file, build-depends, exposed-modules, other-modules, common-stanza, cabal-version, ghc-options, hs-source-dirs, cabal-file-anatomy, haskell-cabal]
level: practitioner
status: docs-checked
description: "Write a package .cabal file: cabal-version, library/executable/test-suite stanzas, build-depends bounds, common stanzas, ghc-options and module lists."
sources: ["https://cabal.readthedocs.io/en/stable/cabal-package-description-file.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# The .cabal file

**Goal:** describe a package so `cabal build` works reproducibly. File: `<name>.cabal` at the package root.

```cabal
cabal-version:      3.0
name:               myapp
version:            0.1.0.0
build-type:         Simple
license:            BSD-3-Clause

common shared
  default-language: GHC2021
  ghc-options:      -Wall -Wcompat
  build-depends:    base >=4.16 && <5

library
  import:           shared
  hs-source-dirs:   src
  exposed-modules:  MyApp, MyApp.Types
  other-modules:    MyApp.Internal
  build-depends:    containers ^>=0.6, text >=2.0 && <2.2

executable myapp
  import:           shared
  main-is:          Main.hs
  hs-source-dirs:   app
  build-depends:    myapp
  ghc-options:      -threaded -rtsopts "-with-rtsopts=-N"

test-suite myapp-test
  import:           shared
  type:             exitcode-stdio-1.0
  main-is:          Spec.hs
  hs-source-dirs:   test
  build-depends:    myapp, tasty, tasty-hunit
```

## Rules
- `cabal-version` is required; from 2.2 it must be on the very first line. It gates syntax (check the User's Guide for the minimum version of common stanzas and imports).
- `^>=0.6` means `>=0.6 && <0.7` (PVP-style major bound); use bounds on every dependency of a published library.
- `exposed-modules` are public; `other-modules` must list every non-exposed module (GHC's `-Wmissing-home-modules` flags ones that are missing).
- `build-tool-depends` for `hspec-discover`, `alex`, `happy`. `data-files` for runtime assets.
- `cabal check` lints the file for Hackage upload.

## Gotchas
- Tabs and indentation matter; fields in a stanza are indented consistently.
- Always set `default-language` (one of Haskell98, Haskell2010, GHC2021 for GHC 9.2 or later, GHC2024 for 9.10 or later).
- Bound too tight causes solver failures; too loose breaks at build time (use `cabal outdated`, revisions on Hackage).
- `hpack` (`package.yaml`, used by Stack) generates the cabal file; do not edit both.

## Self-check
- [ ] `cabal check` reports no errors.
- [ ] A clean clone builds with `cabal build all`.

## Checked

2026-11-02. Confirmed against the Cabal package description page: cabal-version first-line rule, ^>= meaning, default-language values, common stanzas. Removed or fixed: unsupported Haskell98 and linking claims.
Method: documentation only; no commands were run.
