---
id: computing-software.software-engineering.haskell.haskell-toolchain-versions
name: haskell-toolchain-versions
category: computing-software
field: software-engineering
product: haskell
tags: [haskell, ghc-versions, base-version, boot-libraries, ghc-release-policy, migration, tested-with, stackage-lts, haskell-toolchain-versions]
level: advanced
status: draft
description: "Pick a GHC version, map GHC to base versions, understand boot libraries, upgrade policy and how to migrate across breaking releases."
sources: ["https://downloads.haskell.org/ghc/latest/docs/users_guide/UP", "https://haskell-language-server.readthedocs.io/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# GHC versions, base and boot libraries

**Goal:** choose and upgrade GHC deliberately.

## Concepts
- `base` version tracks GHC (for example GHC 9.4 ships base 4.17, 9.6 ships 4.18, 9.8 ships 4.19, 9.10 ships 4.20; see the release notes table for exact pairs).
- Boot libraries ship with GHC (base, containers, text, bytestring, transformers, mtl, stm, array, deepseq, filepath, directory, process, time, parsec, ghc-prim, template-haskell). You may upgrade some from Hackage; some (ghc, ghc-prim, template-haskell, base) are tied to the compiler.
- GHC releases roughly twice a year; the GHC team recommends a specific version in GHCup (`recommended` tag). Stackage LTS pins a GHC.
- Support policy for libraries: many support the last 3 to 5 major GHC releases; write `tested-with`.

## Migration procedure
```bash
ghcup install ghc <new>
cabal build -w ghc-<new> --allow-newer 2>&1 | tee build.log    # find which deps lack support
cabal outdated
```
Read the GHC migration guide ("Migration guides" on the gitlab wiki and the release notes' "Breaking changes") for the target.
Common breakages: `Semigroup`/`Monoid` (8.4), MonadFail (8.8), simplified subsumption (9.0), `forall` keyword/`TypeApplications` rules, `StarIsType`/`Type` kinds, base `Foldable1`, partial function warnings (`-Wx-partial`) (check release for exact numbers).

## Gotchas
- Deprecation warnings become errors under `-Werror`; use `-Werror` only in CI, not in published packages.
- Compat via `base-compat`, `transformers-compat`, `CPP`.
- Template Haskell and Cabal setup scripts break most on major upgrades.
- Keep a changelog of the supported range.

## Self-check
- [ ] CI builds with oldest and newest supported GHC.
- [ ] `ghc --info` shows the expected library dir for the toolchain used.
