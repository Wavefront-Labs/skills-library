---
id: computing-software.software-engineering.haskell.functor-and-applicative
name: functor-and-applicative
category: computing-software
field: software-engineering
product: haskell
tags: [haskell, functor, applicative, fmap, pure, lifta2, applicativestyle, ziplist, alternative, functor-and-applicative, haskell-functor-monad]
level: practitioner
status: draft
description: "Use fmap, <$>, <*>, pure, liftA2 and Alternative; applicative style for independent effects; laws and ZipList."
sources: ["https://hackage.haskell.org/package/base", "https://www.haskell.org/onlinereport/haskell2010/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Functor and Applicative

**Goal:** apply functions inside contexts without monadic sequencing.

```haskell
import Control.Applicative

fmap (+1) (Just 2)                 -- Just 3;  (+1) <$> Just 2
(+) <$> Just 1 <*> Just 2          -- Just 3
liftA2 (,) [1,2] "ab"              -- [(1,'a'),(1,'b'),(2,'a'),(2,'b')]
pure 5 :: Maybe Int                -- Just 5
Just 1 <* Just 2; Just 1 *> Just 2 -- Just 1; Just 2 (sequence, keep one side)
getZipList (ZipList [(+1),(*2)] <*> ZipList [10,20])   -- [11,40]
Nothing <|> Just 3                 -- Just 3 (Alternative: choice)
(,) <$> readA <*> readB            -- IO: runs readA then readB, combines
```

## Laws
- Functor: `fmap id = id`; `fmap (f . g) = fmap f . fmap g`.
- Applicative: identity, composition, homomorphism (`pure f <*> pure x = pure (f x)`), interchange.
- `fmap f x = pure f <*> x`.

## Use
- Applicative is enough when effects do not depend on earlier results; that allows static analysis and
  error accumulation (validation, parsers like optparse-applicative).
- `ApplicativeDo` lets `do` notation desugar to applicative combinators where possible.
- `traverse`/`sequenceA` are applicative-based.

## Gotchas
- `fmap` over a tuple maps the second component only.
- Functions `(->) r` are Functors/Applicatives/Monads (reader); `(+) <$> (*2) <*> (+10)` is a classic puzzle.
- `<$>` is infixl 4, `<*>` infixl 4, `<|>` infixl 3.
- `liftA2` is exported from Prelude only in newer base (unconfirmed which); import `Control.Applicative`.

## Self-check
- [ ] Independent validations use Applicative, not a Monad that stops at the first error.
- [ ] Instances satisfy the laws (checkers package or QuickCheck).
