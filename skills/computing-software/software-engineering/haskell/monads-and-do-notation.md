---
id: computing-software.software-engineering.haskell.monads-and-do-notation
name: monads-and-do-notation
category: computing-software
field: software-engineering
product: haskell
tags: [haskell, monad, do-notation, bind, return, join, maybe-monad, list-monad, desugaring, monads-and-do-notation]
level: intro
status: draft
description: "Understand >>=, return, do notation desugaring, Maybe/Either/list monads, join, when/unless/forM and replicateM, and avoid common do pitfalls."
sources: ["https://hackage.haskell.org/package/base", "https://www.haskell.org/onlinereport/haskell2010/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Monads and do notation

**Goal:** sequence dependent computations and read `do` as sugar over `>>=`.

```haskell
safeDiv :: Int -> Int -> Maybe Int
safeDiv _ 0 = Nothing
safeDiv a b = Just (a `div` b)

calc :: Maybe Int
calc = do
  a <- safeDiv 100 5
  b <- safeDiv a 2
  let c = a + b            -- let in do: no 'in'
  return (c * 2)           -- same as pure

-- desugaring: safeDiv 100 5 >>= \a -> safeDiv a 2 >>= \b -> ...
pairs = do { x <- [1,2]; y <- "ab"; return (x, y) }    -- list monad: all combinations
```

## Key functions (Control.Monad)
`>>=`, `>>`, `return`/`pure`, `join`, `=<<`, `>=>` (Kleisli), `when`, `unless`, `forM`/`forM_`, `replicateM`,
`replicateM_`, `foldM`, `zipWithM`, `filterM`, `void`, `forever`, `guard` (MonadPlus/Alternative), `mapM_`.

## Laws
Left identity `return a >>= f == f a`; right identity `m >>= return == m`; associativity
`(m >>= f) >>= g == m >>= (\x -> f x >>= g)`.

## Gotchas
- The last statement of a `do` block must be an expression, not `x <- ...`.
- `return` does not exit; `return 1 >> return 2` yields 2.
- A pattern bind that can fail (`Just x <- m`) calls `fail` (MonadFail) in the monad; in `IO` it throws, in Maybe/list it short circuits.
- `forever` needs an exit by exception or `Maybe`/`Either` short-circuit.
- `mapM`/`forM` on huge lists in a lazy monad can leak; use `foldM` or streaming.

## Self-check
- [ ] Can desugar a three-line `do` by hand to `>>=` chains.
- [ ] `guard` used in list/Maybe monads instead of nested ifs.
