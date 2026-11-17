---
id: computing-software.software-engineering.haskell.deriving-strategies-and-via
name: deriving-strategies-and-via
category: computing-software
field: software-engineering
product: haskell
tags: [haskell, deriving, derivingstrategies, derivinganyclass, derivingvia, derivefunctor, derivegeneric, standalone-deriving, deriving-strategies-and-via]
level: advanced
status: docs-checked
description: "Use stock, newtype, anyclass and via deriving strategies, DeriveFunctor/Foldable/Traversable/Generic, and StandaloneDeriving, with ambiguity rules."
sources: ["https://www.haskell.org/onlinereport/haskell2010/", "https://downloads.haskell.org/ghc/latest/docs/users_guide/exts/deriving_strategies.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Deriving strategies

**Goal:** let GHC generate instances and choose the strategy explicitly.

```haskell
{-# LANGUAGE DerivingStrategies, DeriveAnyClass, DerivingVia, GeneralizedNewtypeDeriving,
             DeriveGeneric, DeriveFunctor, DeriveFoldable, DeriveTraversable, StandaloneDeriving #-}
import GHC.Generics (Generic)
import Data.Monoid (Sum(..))

data T a = T a [a]
  deriving stock (Show, Eq, Ord, Functor, Foldable, Traversable, Generic)

newtype Age = Age Int
  deriving newtype (Eq, Ord, Num)           -- reuse Int's instance
  deriving stock Show

newtype Total = Total Int
  deriving (Semigroup, Monoid) via (Sum Int)   -- DerivingVia: borrow another type's instance

data Cfg = Cfg { a :: Int } deriving stock Generic
                            deriving anyclass ToJSON   -- anyclass uses the class's default signatures

deriving instance Show (f (Fix f)) => Show (Fix f)     -- standalone
```

## Stock-derivable classes
`Eq, Ord, Enum, Bounded, Show, Read, Ix` (Haskell 2010), plus `Functor, Foldable, Traversable, Generic, Data, Lift`
with extensions.

## Gotchas
- Without a strategy, GHC guesses; with both DeriveAnyClass and GeneralizedNewtypeDeriving on, it favours DeriveAnyClass (and warns under `-Wderiving-defaults`), which leaves you unable to use both in one module. Always write the strategy.
- `DerivingStrategies` is included in the GHC2024 edition but not GHC2021.
- DeriveFunctor requires the type parameter in the last position.
- Derived `Ord` compares constructors in declaration order.

## Self-check
- [ ] Every `deriving` clause names a strategy in code with several extensions on.
- [ ] `-Wderiving-defaults` is silent.

## Checked

2026-11-02. Confirmed against the GHC User's Guide exts/deriving_strategies page: ambiguity rule favouring DeriveAnyClass, -Wderiving-defaults, GHC2024 membership. Removed or fixed: unsupported precedence and Read speed sentences.
Method: documentation only; no commands were run.
