---
id: computing-software.software-engineering.haskell.ghc-generics-datatype-generic
name: ghc-generics-datatype-generic
category: computing-software
field: software-engineering
product: haskell
tags: [haskell, generics, ghc-generics, rep, from-to, datatype-generic, deriving-anyclass, generic-default, generic-deriving, ghc-generics-datatype-generic, haskell-generics]
level: sme
status: docs-checked
description: "Write generic functions over GHC.Generics representations (M1, K1, :+:, :*:), default signatures, and derive instances via DeriveAnyClass."
sources: ["https://downloads.haskell.org/ghc/latest/docs/users_guide/exts/generics.html", "https://hackage.haskell.org/package/base/docs/GHC-Generics.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GHC.Generics

**Goal:** write one function that works for all algebraic types.

```haskell
{-# LANGUAGE DeriveGeneric, DeriveAnyClass, DefaultSignatures, FlexibleContexts, TypeOperators, ScopedTypeVariables #-}
import GHC.Generics

class Encode a where
  encode :: a -> [Int]
  default encode :: (Generic a, GEncode (Rep a)) => a -> [Int]
  encode = gencode . from

class GEncode f where gencode :: f p -> [Int]
instance GEncode V1 where gencode _ = []
instance GEncode U1 where gencode U1 = []
instance (GEncode a, GEncode b) => GEncode (a :*: b) where gencode (a :*: b) = gencode a ++ gencode b
instance (GEncode a, GEncode b) => GEncode (a :+: b) where
  gencode (L1 x) = 0 : gencode x
  gencode (R1 x) = 1 : gencode x
instance GEncode a => GEncode (M1 i c a) where gencode (M1 x) = gencode x   -- metadata wrapper
instance Encode a => GEncode (K1 i a) where gencode (K1 x) = encode x

instance Encode Int where encode n = [n]
data T = A Int | B Int Int deriving (Generic, Encode)     -- DeriveAnyClass uses the default
```

## Concepts
- `Rep a` is the sum-of-products structure: `:+:` constructors, `:*:` fields, `U1` unit, `V1` void, `K1` field, `M1` metadata (`D`atatype, `C`onstructor, `S`elector). Metadata names via `datatypeName`, `conName`, `selName`.
- `from :: a -> Rep a x`, `to :: Rep a x -> a`.
- Example libraries built on it (check each on Hackage): aeson, binary, cereal, deepseq (NFData), hashable, generic-lens, `generic-random`, `generics-sop` (simpler n-ary view).

## Gotchas
- Large types produce deeply nested balanced `:+:`/`:*:`, increasing compile time; derive Generic only where needed.
- Use `INLINE` pragmas on `from`-based defaults for performance, since Generic code is slow if not optimised away.
- Error messages are unreadable; build generic functions incrementally and test on small types.

## Self-check
- [ ] Generic default works for a sum type and a record.
- [ ] Hand-written instance still overrides when needed.

## Checked

2026-11-02. Confirmed against the GHC User's Guide exts/generics; base GHC.Generics docs: Rep structure, datatypeName/conName/selName. Removed or fixed: library list marked as examples.
Method: documentation only; no commands were run.
