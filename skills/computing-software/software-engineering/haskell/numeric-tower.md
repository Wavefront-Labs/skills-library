---
id: computing-software.software-engineering.haskell.numeric-tower
name: numeric-tower
category: computing-software
field: software-engineering
product: haskell
tags: [haskell, int, integer, double, rational, fromintegral, realtofrac, num-hierarchy, word, overflow, numeric-tower]
level: practitioner
status: docs-checked
description: "Choose among Int, Integer, Word, Double and Rational, convert with fromIntegral and realToFrac, and read round, div and quot correctly."
sources: ["https://hackage.haskell.org/package/base", "https://www.haskell.org/onlinereport/haskell2010/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Numeric types and conversions

**Goal:** pick a numeric type and convert without silent errors.

## Types
- `Int`: fixed-width integer, bounded by `minBound` and `maxBound`.
- `Integer`: arbitrary precision. `Word`, `Int8..Int64`, `Word8..Word64` in `Data.Int`/`Data.Word`.
- `Double`, `Float`: IEEE floating point. `Rational` = `Ratio Integer` (`3 % 4`, `Data.Ratio`).
- `Natural` (in `Numeric.Natural`): arbitrary-precision natural number; `minusNaturalMaybe` subtracts without going below zero.

## Class hierarchy
`Num` (+, *, abs, signum, fromInteger, negate) -> `Real` (toRational) -> `Integral` (div, mod, quot, rem, toInteger);
`Fractional` (/, fromRational) -> `Floating` (pi, exp, sqrt, sin) ; `RealFrac` (floor, ceiling, round, truncate).

## Conversions
```haskell
fromIntegral (n :: Int) :: Double      -- integral to any Num
realToFrac (x :: Float) :: Double      -- real to fractional
round 2.5 :: Int                       -- 2: the even integer when equidistant
floor (-1.5) :: Int                    -- -2
x `div` y; x `mod` y                   -- round toward negative infinity
x `quot` y; x `rem` y                  -- truncate toward zero
2 ^ 10; 2 ** 0.5; 2 ^^ (-1)            -- Integral exponent, floating, negative integral
```

## Gotchas
- Fixed-width types such as `Int` are bounded (`minBound`, `maxBound`); use `Integer` when the range may be exceeded.
- `div` truncates toward negative infinity and `quot` toward zero; pick the one you mean for negative operands.

## Self-check
- [ ] `maxBound :: Int` consequences considered for counters and hashes.
- [ ] Numeric literals in ambiguous positions carry a type annotation.

## Checked

2026-11-03. Confirmed against base Prelude, Data.Int, Data.Word, Numeric.Natural and Data.Ratio pages: round to even, div/quot semantics, minusNaturalMaybe, fromIntegral and realToFrac. Removed: Int width and overflow claims, Scientific description, money advice, defaulting-warning claims.
Method: documentation only; no commands were run.
