---
id: computing-software.software-engineering.haskell.gadts-and-existentials
name: gadts-and-existentials
category: computing-software
field: software-engineering
product: haskell
tags: [haskell, gadts, existential-types, existentialquantification, type-refinement, typed-expression-evaluator, gadts-and-existentials, haskell-advtypes]
level: advanced
status: docs-checked
description: "Declare GADTs with type refinement for typed interpreters, existential wrappers with forall, and know the MonoLocalBinds and type-signature requirements."
sources: ["https://downloads.haskell.org/ghc/latest/docs/users_guide/exts/gadt.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GADTs and existentials

**Goal:** encode invariants in constructor return types and hide types behind classes.

```haskell
{-# LANGUAGE GADTs, KindSignatures, RankNTypes, ExistentialQuantification #-}
data Expr :: * -> * where              -- or: data Expr a where  (Type from Data.Kind is preferred over *)
  IntE  :: Int  -> Expr Int
  BoolE :: Bool -> Expr Bool
  Add   :: Expr Int -> Expr Int -> Expr Int
  If    :: Expr Bool -> Expr a -> Expr a -> Expr a
  Eq    :: Expr Int -> Expr Int -> Expr Bool

eval :: Expr a -> a                    -- a signature is REQUIRED for GADT matches
eval (IntE n) = n
eval (Add a b) = eval a + eval b
eval (If c t e) = if eval c then eval t else eval e
eval (Eq a b) = eval a == eval b

data Showable = forall a. Show a => MkShowable a       -- existential: type hidden, dictionary kept
shows' (MkShowable a) = show a
```

## Facts
- Matching on a GADT constructor refines type variables in that branch.
- GADTs implies MonoLocalBinds and GADTSyntax; it is part of GHC2024 but not GHC2021 (GADTSyntax plus ExistentialQuantification, both in GHC2021, suffice to define and use GADTs).
- The existential can only be used through its class methods; cannot return the hidden type.
- `data Some where Some :: Show a => a -> Some` is the GADT syntax for the same existential.
- Import `Data.Kind (Type)`; write `data Expr :: Type -> Type`.

## Gotchas
- Deriving instances for GADTs needs `StandaloneDeriving`, and may need `deriving instance Show (Expr a)`.
- Type inference is weaker: annotate local functions.
- Heterogeneous lists of existentials lose type information; consider `Data.Dynamic`/`Typeable` for runtime checks.

## Self-check
- [ ] Interpreter has total `eval :: Expr a -> a` with `-Wall` clean (impossible cases do not need patterns).
- [ ] Existential wrappers expose only class methods.

## Checked

2026-11-02. Confirmed against the GHC User's Guide exts/gadt page: GADTs implies MonoLocalBinds and GADTSyntax, edition membership. Removed or fixed: Functor deriving claim.
Method: documentation only; no commands were run.
