---
id: computing-software.software-engineering.haskell.point-free-and-composition
name: point-free-and-composition
category: computing-software
field: software-engineering
product: haskell
tags: [haskell, composition, point-free, dot-operator, dollar, ampersand, eta-reduction, point-free-and-composition]
level: practitioner
status: draft
description: "Compose functions with (.) and ($), use (&) and on from Data.Function, eta-reduce sensibly and know when point-free style hurts readability."
sources: ["https://www.haskell.org/onlinereport/haskell2010/", "https://hackage.haskell.org/package/base"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Composition and point-free style

**Goal:** build pipelines from small functions without obscuring intent.

```haskell
import Data.Function ((&), on)
import Data.Char (toUpper)
import Data.List (sortBy)

shout :: String -> String
shout = map toUpper . filter (/= ' ')      -- (f . g) x = f (g x)

total :: [Int] -> Int
total xs = xs & filter even & map (* 2) & sum    -- left-to-right pipeline with &

byLen :: [String] -> [String]
byLen = sortBy (compare `on` length)             -- `on` lifts a projection

main = print $ sum $ map (* 2) [1..10]           -- $ avoids parentheses
```

## Rules
- `.` is `infixr 9`, `$` is `infixr 0`, `&` is `infixl 1`.
- Point-free is eta reduction: `f x = g (h x)` becomes `f = g . h`.
- Cryptic combinators like `(.) . (.)` exist; prefer a named lambda.
- `flip`, `const`, `id`, `uncurry` are the usual glue.

## Gotchas
- `f . g $ x` is fine; `f $ g . h $ x` mixes badly and often fails to type check.
- Point-free top-level definitions interact with the monomorphism restriction: always add a signature.
- With RankNTypes, `$` has special typing support for higher-rank arguments; `.` does not.
- Deep point-free chains give poor error messages and make stepping in the debugger harder.

## Self-check
- [ ] Each pipeline stage has a type that can be checked with `:t` in GHCi.
- [ ] A reader can name the intermediate values; if not, use a `where` binding.
