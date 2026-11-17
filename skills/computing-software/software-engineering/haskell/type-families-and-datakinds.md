---
id: computing-software.software-engineering.haskell.type-families-and-datakinds
name: type-families-and-datakinds
category: computing-software
field: software-engineering
product: haskell
tags: [haskell, typefamilies, datakinds, closed-type-families, associated-types, kinds, typenats, type-level, singletons, polykinds, type-families-and-datakinds]
level: sme
status: docs-checked
description: "Use type families, associated types, DataKinds promoted data, kind signatures and GHC.TypeLits for type-level programming, with the known costs."
sources: ["https://downloads.haskell.org/ghc/latest/docs/users_guide/exts/type_families.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Type families, DataKinds and kinds

**Goal:** compute with types where the invariant is worth the complexity.

```haskell
{-# LANGUAGE TypeFamilies, DataKinds, KindSignatures, GADTs, TypeOperators, UndecidableInstances #-}
import Data.Kind (Type)
import GHC.TypeLits

type family Elem c :: Type                       -- open type family
type instance Elem [a] = a

type family If (c :: Bool) (t :: k) (e :: k) :: k where   -- closed: equations tried in order
  If 'True  t e = t
  If 'False t e = e

class Container f where
  type Item f :: Type                            -- associated type
  empty  :: f
  insert :: Item f -> f -> f

data Nat' = Z | S Nat'
data Vec (n :: Nat') a where                     -- DataKinds: Nat' promoted to a kind
  VNil  :: Vec 'Z a
  VCons :: a -> Vec n a -> Vec ('S n) a

vhead :: Vec ('S n) a -> a                       -- total: empty vector is a type error
vhead (VCons x _) = x

newtype Tagged (s :: Symbol) = Tagged Int        -- type-level string; symbolVal (Proxy @s) at run time
```

## Facts
- `Nat` and `Symbol` from `GHC.TypeLits` (type-level literals, `natVal`, `symbolVal`, `KnownNat`); solving arithmetic like `n + 1 ~ m` needs plugins (e.g. ghc-typelits-natnormalise).
- Data families (`data family`) define new data types per index. Type-equality constraint `a ~ b` is available.
- PolyKinds makes kinds polymorphic; in GHC2021 and GHC2024. DataKinds is in GHC2024 only.

## Gotchas
- Type families are not injective by default; `TypeFamilyDependencies` can add `= r | r -> a`.
- Error messages are long; give signatures and `-fprint-explicit-kinds` when debugging.
- Compile time rises with heavy type-level code.
- Prefer ordinary values and smart constructors unless the guarantee prevents real bugs.

## Self-check
- [ ] Each type-level device removes a runtime check or invalid state you can name.
- [ ] Module compiles with `-Wall` and no `UndecidableInstances` unless justified.

## Checked

2026-11-02. Confirmed against the GHC User's Guide exts/type_families and control pages: TypeFamilyDependencies, PolyKinds and DataKinds edition membership. Removed or fixed: none.
Method: documentation only; no commands were run.
