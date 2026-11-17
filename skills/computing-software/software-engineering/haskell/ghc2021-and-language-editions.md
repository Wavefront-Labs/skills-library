---
id: computing-software.software-engineering.haskell.ghc2021-and-language-editions
name: ghc2021-and-language-editions
category: computing-software
field: software-engineering
product: haskell
tags: [haskell, ghc2021, haskell2010, default-extensions, default-language, language-pragma, editions, ghc2021-and-language-editions, haskell-extensions]
level: practitioner
status: docs-checked
description: "Choose a language edition (Haskell2010 or GHC2021) and manage extensions via LANGUAGE pragmas and default-extensions in the cabal file."
sources: ["https://downloads.haskell.org/ghc/latest/docs/users_guide/exts/control.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Language editions and extensions

**Goal:** know what extensions are on by default and manage them centrally.

## Editions
- `Haskell98`, `Haskell2010`, `GHC2021` (since GHC 9.2.1; used by default when no edition is requested) and `GHC2024` (since GHC 9.10.1; the User's Guide recommends it for new code and advises declaring the edition explicitly). Selecting an edition overrides any earlier one and cannot be undone.
  Set `default-language` explicitly in each cabal stanza; check what `cabal init` generated.
- GHC2021 adds a bundle of widely used extensions such as `BangPatterns`, `ScopedTypeVariables`, `TypeApplications`, `FlexibleContexts`,
  `FlexibleInstances`, `GeneralisedNewtypeDeriving`, `DeriveFunctor`/`Generic`/`Traversable`, `StandaloneDeriving`, `TupleSections`, `KindSignatures`, `RankNTypes`, `InstanceSigs`. The exact list is in the GHC User's Guide; read it for your GHC version.
- Not in GHC2021 (needs a pragma): `LambdaCase`, `OverloadedStrings`, `GADTs`, `TypeFamilies`, `DataKinds`, `RecordWildCards`, `DerivingStrategies`, `DeriveAnyClass`. GHC2024 adds `LambdaCase`, `GADTs`, `DataKinds`, `DerivingStrategies` (among others) but still not `OverloadedStrings`, `TypeFamilies`, `RecordWildCards` or `DeriveAnyClass`.

## Where to enable
```
-- per file
{-# LANGUAGE LambdaCase #-}

-- per package (mypkg.cabal), per stanza
library
  default-language: GHC2021
  default-extensions: LambdaCase, OverloadedStrings, DerivingStrategies
```
```bash
ghc -XLambdaCase App.hs          # command line
ghci> :set -XOverloadedStrings   # in GHCi
ghci> :show language
```

## Gotchas
- Extensions in `default-extensions` hide which file needs which; keep the list short and conventional.
- Turn off with `NoImplicitPrelude`, `NoMonomorphismRestriction`.
- Some extensions change semantics (Strict, StrictData, MonoLocalBinds, NoFieldSelectors); others only add syntax.
- Libraries targeting old GHC versions should avoid `GHC2021` (needs GHC 9.2.1 or later) and `GHC2024` (9.10.1 or later).
- `Safe`, `Trustworthy` are Safe Haskell flags, not feature extensions.

## Self-check
- [ ] The cabal file has `default-language` in every stanza.
- [ ] `ghc --supported-extensions` lists every extension you use.

## Checked

2026-11-02. Confirmed against the GHC User's Guide exts/control page; Cabal package description: GHC2021 and GHC2024 extension lists, edition rules. Removed or fixed: mandatory-ish default-language claim; added GHC2024.
Method: documentation only; no commands were run.
