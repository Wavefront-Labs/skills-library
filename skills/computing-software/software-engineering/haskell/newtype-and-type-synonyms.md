---
id: computing-software.software-engineering.haskell.newtype-and-type-synonyms
name: newtype-and-type-synonyms
category: computing-software
field: software-engineering
product: haskell
tags: [haskell, newtype, type-synonym, data, zero-cost, coerce, generalizednewtypederiving, newtype-and-type-synonyms]
level: intro
status: docs-checked
description: "Choose between type synonyms, newtype and data, use newtype for zero-cost wrappers with GeneralizedNewtypeDeriving and coerce, and know the strictness difference."
sources: ["https://www.haskell.org/onlinereport/haskell2010/haskellch4.html", "https://www.haskell.org/onlinereport/haskell2010/haskellch3.html", "https://downloads.haskell.org/ghc/latest/docs/users_guide/exts/newtype_deriving.html", "https://downloads.haskell.org/ghc/latest/docs/users_guide/exts/deriving_strategies.html", "https://hackage.haskell.org/package/base/docs/Data-Coerce.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# type, newtype and data

**Goal:** model domain types cheaply and safely.

```haskell
type Name = String                         -- synonym: same type, only an alias
newtype UserId = UserId Int deriving (Eq, Ord, Show)    -- distinct type, no runtime cost
newtype Age = Age { getAge :: Int }
data Pair = Pair Int Int                   -- ordinary boxed data
```

## Differences
- `type` is a synonym: `Name` and `String` are the same type. New instances may not be defined for a type synonym.
- `newtype` has exactly one constructor with exactly one field; it creates a distinct type, and the coercions may be
  implemented without execution time overhead, so `newtype` adds type safety for free.
- The newtype constructor is unlifted, so `N undefined` is the same as `undefined`: pattern matching a newtype
  constructor forces nothing, whereas matching a `data` constructor does.
- A newtype can have its own class instances, unlike a synonym, and may define a recursive type.

## Deriving through newtypes
```haskell
{-# LANGUAGE GeneralizedNewtypeDeriving, DerivingStrategies #-}
import Data.Coerce (coerce)
newtype Score = Score Int deriving newtype (Eq, Ord, Num, Show)
coerce [Score 1, Score 2] :: [Int]         -- zero-cost conversion of the whole list
```
`coerce` needs the newtype constructor in scope and respects role annotations (`type role Set nominal` blocks it).
GeneralizedNewtypeDeriving is included in GHC2021; DerivingStrategies (needed for the `deriving newtype` syntax) is
included in GHC2024 but not GHC2021.

## Gotchas
- `deriving newtype Show` reuses the underlying type's instance, so the output has no constructor name; stock `deriving Show` prints the constructor name.
- Newtype deriving of a class is safe only when the class's missing last argument is not used at a nominal role in any method.
- Use `newtype` for wrappers like `Sum`, `Product`, `Down`, `Identity` from base.

## Self-check
- [ ] Domain identifiers (ids, units) are newtypes, not bare `Int`/`String`.

## Checked

2026-11-08. Confirmed against the Haskell 2010 Report (section 4.2.3 type synonyms, newtype and data differences; section 3.17 pattern matching of newtype constructors; chapter 11 stock `Show` output), the GHC User's Guide pages for GeneralisedNewtypeDeriving (edition membership, role condition) and deriving strategies (`deriving newtype`, edition membership), and the base `Data.Coerce` page (constructor in scope, `type role`). Removed: LiberalTypeSynonyms and TypeSynonymInstances claims and the `-ddump-simpl` self-check (not in the pages read). Fixed: the pragma list now includes DerivingStrategies.
Method: documentation only; no commands were run.
