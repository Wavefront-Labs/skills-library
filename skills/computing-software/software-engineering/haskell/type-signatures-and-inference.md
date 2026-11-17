---
id: computing-software.software-engineering.haskell.type-signatures-and-inference
name: type-signatures-and-inference
category: computing-software
field: software-engineering
product: haskell
tags: [haskell, type-signature, type-inference, monomorphism-restriction, defaulting, hindley-milner, type-signatures-and-inference, haskell-types-basic]
level: intro
status: draft
description: "Write top-level signatures, read inferred types in GHCi, and handle the monomorphism restriction and numeric defaulting rules."
sources: ["https://www.haskell.org/onlinereport/haskell2010/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Signatures, inference and defaulting

**Goal:** know when GHC infers a type, when to annotate, and why a binding becomes `Integer` unexpectedly.

```haskell
double :: Num a => a -> a        -- signature with a class constraint
double x = x * 2

plus = (+)                       -- NO signature: monomorphism restriction applies
-- plus :: Integer -> Integer -> Integer after defaulting (unless used at another type)
```
In GHCi: `:t expr`, `:i Name`, `:k Type` for kinds, `:set +t` to print types of results.

## Rules
- Haskell 2010 infers types (Hindley-Milner with classes); signatures are optional but standard for all
  top-level bindings.
- Monomorphism restriction: a pattern or simple binding without arguments and without a signature is not
  generalised over constrained type variables; defaulting then picks `Integer` or `Double`.
  `NoMonomorphismRestriction` disables it (GHCi has it off by default).
- Defaulting resolves ambiguous `Num`/`Show` constraints (`show (2^10)`). `-Wtype-defaults` (in `-Wall`) warns.
- `ExtendedDefaultRules` is only for GHCi-like use.

## Typed holes
Write `_` or `_name` in an expression; GHC reports the expected type and valid fits. Use
`-fdefer-typed-holes` to compile and fail only if the hole is evaluated.

## Gotchas
- `ScopedTypeVariables` is needed for a local signature to mention an outer type variable; the outer signature
  needs an explicit `forall`.
- `read "5"` needs a type annotation: `read "5" :: Int`.
- Ambiguous type error: `show (read s)` has no determined type.

## Self-check
- [ ] Every top-level definition has a signature (`-Wmissing-signatures`, in `-Wall`).
- [ ] No `-Wtype-defaults` warnings left unexplained.
