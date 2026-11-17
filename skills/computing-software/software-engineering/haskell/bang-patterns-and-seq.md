---
id: computing-software.software-engineering.haskell.bang-patterns-and-seq
name: bang-patterns-and-seq
category: computing-software
field: software-engineering
product: haskell
tags: [haskell, bangpatterns, seq, strict-fields, whnf, strictdata, dollar-bang, bang-patterns-and-seq, haskell-laziness]
level: practitioner
status: docs-checked
description: "Force evaluation with seq, $!, bang patterns and strict constructor fields, and understand WHNF so accumulators and records do not build thunks."
sources: ["https://downloads.haskell.org/ghc/latest/docs/users_guide/exts/strict.html", "https://hackage.haskell.org/package//deepseq"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# seq, bang patterns and strict fields

**Goal:** control when values are evaluated.

```haskell
{-# LANGUAGE BangPatterns #-}
mean :: [Double] -> Double
mean = go 0 0
  where
    go !s !n []     = s / fromIntegral (n :: Int)   -- bangs force accumulators each step
    go !s !n (x:xs) = go (s + x) (n + 1) xs

f x = x `seq` x + 1        -- evaluate x to WHNF, then continue
g = foldl' (+) 0 . map (* 2)
y = f $! expensive         -- f $! x = x `seq` f x

data P = P !Int !Int       -- strict fields: evaluated on construction
```

## Facts
- WHNF = weak head normal form: outermost constructor or lambda evaluated, fields not. `seq` only goes that far.
- `StrictData` makes every field in the module strict; `Strict` also makes bindings and patterns strict (use
  sparingly; it changes semantics).
- `let !x = e in body` forces `e` before `body`.
- Strict fields cost an extra evaluation at construction and can add `UNPACK` benefits: `data P = P {-# UNPACK #-} !Int`.

## Gotchas
- A bang on a tuple pattern `!(a, b)` forces only the tuple, not `a` and `b`.
- Strictness annotations can change termination: forcing an undefined or infinite value now diverges.
- `seq a b` does not guarantee a is evaluated before b in the sense of IO ordering; it only ties demand.

## Self-check
- [ ] `+RTS -s` for the accumulator loop shows small max residency (no growing thunk chain).
- [ ] Strict fields used for numeric hot-path records; lazy fields kept where laziness is needed.

## Checked

2026-11-02. Confirmed against the GHC User's Guide exts/strict page: BangPatterns semantics, let !x, StrictData and Strict. Removed or fixed: none.
Method: documentation only; no commands were run.
