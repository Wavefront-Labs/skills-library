---
id: computing-software.software-engineering.haskell.algebraic-data-types
name: algebraic-data-types
category: computing-software
field: software-engineering
product: haskell
tags: [haskell, adt, sum-type, product-type, data-declaration, maybe, either, recursive-types, algebraic-data-types]
level: intro
status: docs-checked
description: "Define sum and product types with data, parameterised and recursive types, and encode invalid states as unrepresentable using Maybe, Either and NonEmpty."
sources: ["https://www.haskell.org/onlinereport/haskell2010/haskellch6.html", "https://www.haskell.org/onlinereport/haskell2010/haskellch11.html", "https://hackage.haskell.org/package/base/docs/Data-List-NonEmpty.html", "https://downloads.haskell.org/ghc/latest/docs/users_guide/using-warnings.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Algebraic data types

**Goal:** model data so illegal states do not type check.

```haskell
data Colour = Red | Green | Blue deriving (Show, Eq, Ord, Enum, Bounded)   -- enumeration
data Shape  = Circle Double | Rect Double Double                            -- sum of products
data Tree a = Leaf | Node (Tree a) a (Tree a) deriving Show                 -- recursive, parameterised

insert :: Ord a => a -> Tree a -> Tree a
insert x Leaf = Node Leaf x Leaf
insert x t@(Node l v r)
  | x < v = Node (insert x l) v r
  | x > v = Node l v (insert x r)
  | otherwise = t

-- standard library ADTs
-- data Maybe a = Nothing | Just a
-- data Either a b = Left a | Right b
```

## Practices
- Prefer many small constructors to a record of `Maybe`s: `data Conn = Closed | Open Handle` rather than
  `{ isOpen :: Bool, handle :: Maybe Handle }`.
- Use `Data.List.NonEmpty` (`data NonEmpty a = a :| [a]`) for "at least one" invariants.
- `[minBound .. maxBound] :: [Colour]` lists an enumeration (needs `Enum` and `Bounded`).
- Existential and GADT forms are covered in the GADTs skill.

## Gotchas
- Positional constructor fields become unreadable as they multiply; switch to records.
- A recursive type needs a base case constructor (`Leaf`) or it cannot be built.
- Deriving `Ord` compares lexicographically with earlier constructors smaller than later ones; reorder constructors with care.
- Derived `Show` parenthesises according to precedence (`showsPrec d x r`, d from 0 to 11); for infix constructors, associativity is not used to reduce parentheses.
- Deriving `Enum` works only for enumerations, `Bounded` for enumerations and single-constructor types.

## Self-check
- [ ] Adding a constructor triggers `-Wincomplete-patterns` warnings at every consumer.
- [ ] No boolean flags that make some field combinations meaningless.

## Checked

2026-11-08. Confirmed against the Haskell 2010 Report (chapter 6 predefined types for Maybe and Either, chapter 11 derived instances for Eq, Ord, Enum, Bounded, Show and showsPrec behaviour), the base documentation for NonEmpty, and the GHC warnings page for `-Wincomplete-patterns`. Removed: the numeric "3 or 4 fields" threshold and the negative-number parenthesis claim.
Method: documentation only; no commands were run.
