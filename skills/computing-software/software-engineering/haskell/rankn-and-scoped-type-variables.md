---
id: computing-software.software-engineering.haskell.rankn-and-scoped-type-variables
name: rankn-and-scoped-type-variables
category: computing-software
field: software-engineering
product: haskell
tags: [haskell, rankntypes, scopedtypevariables, typeapplications, forall, higher-rank, allowambiguoustypes, visible-type-application, rankn-and-scoped-type-variables]
level: advanced
status: docs-checked
description: "Use forall for higher-rank types, ScopedTypeVariables with explicit forall, and TypeApplications (@Int) to select types without annotations."
sources: ["https://downloads.haskell.org/ghc/latest/docs/users_guide/exts/scoped_type_variables.html", "https://downloads.haskell.org/ghc/latest/docs/users_guide/exts/rank_polymorphism.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# RankNTypes, ScopedTypeVariables, TypeApplications

**Goal:** control quantification so signatures say what you mean.

```haskell
{-# LANGUAGE RankNTypes, ScopedTypeVariables, TypeApplications, AllowAmbiguousTypes #-}

applyAll :: (forall a. [a] -> Int) -> ([Int], String) -> (Int, Int)   -- rank-2: argument is polymorphic
applyAll f (xs, s) = (f xs, f s)

sizeOf' :: forall a. (Bounded a, Enum a) => Int       -- 'a' scoped over the body
sizeOf' = fromEnum (maxBound @a) - fromEnum (minBound @a) + 1

go :: forall a. Show a => [a] -> String
go xs = concatMap f xs where
  f :: a -> String                -- refers to the outer a thanks to forall
  f = show

read @Int "5"                      -- visible type application
show @Double 3
maxBound @Word8
sizeOf' @Bool                       -- needs AllowAmbiguousTypes on the definition
```

## Rules
- Without `forall` in the signature, an inner signature's `a` is a fresh variable (a classic error:
  "Couldn't match type a1 with a").
- ScopedTypeVariables also scopes pattern signatures: `\(x :: Int) -> ...`.
- Type application order follows the left-to-right order of the explicit `forall` (or first appearance); a signature
  with an explicit forall fixes it. Use `forall a b.` to document.
- GHC2021 (and GHC2024) enable ScopedTypeVariables, TypeApplications, ExplicitForAll and RankNTypes; AllowAmbiguousTypes is not included.

## Gotchas
- Type inference for rank-N needs signatures; passing `(.)`-composed polymorphic functions often fails.
- Impredicative types (`[forall a. a -> a]`) need `ImpredicativeTypes` (see the User's Guide section on impredicative polymorphism for the Quick Look rules and the GHC version).
- Changing the order of type variables in an exported signature breaks users of `@` application.

## Self-check
- [ ] Local signatures that mention outer type variables compile.
- [ ] Library exports document the intended order of type variables.

## Checked

2026-11-02. Confirmed against the GHC User's Guide exts/scoped_type_variables, rank_polymorphism and control pages: forall scoping, GHC2021 membership. Removed or fixed: Quick Look version claim.
Method: documentation only; no commands were run.
