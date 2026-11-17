---
id: computing-software.software-engineering.haskell.deepseq-and-nf
name: deepseq-and-nf
category: computing-software
field: software-engineering
product: haskell
tags: [haskell, deepseq, nfdata, force, rnf, normal-form, evaluate, rwhnf, deepseq-and-nf]
level: practitioner
status: docs-checked
description: "Fully evaluate structures with Control.DeepSeq: NFData instances via Generic, deepseq, force and evaluate, plus when whole-structure forcing is wasteful."
sources: ["https://downloads.haskell.org/ghc/latest/docs/users_guide/", "https://hackage.haskell.org/package//deepseq"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# deepseq and normal form

**Goal:** force a value completely (normal form), e.g. before timing, to avoid thunks escaping a thread, or to make exceptions occur at a known point.

```haskell
{-# LANGUAGE DeriveGeneric, DeriveAnyClass #-}
import Control.DeepSeq
import Control.Exception (evaluate)
import GHC.Generics (Generic)

data Tree = Leaf | Node Tree Int Tree deriving (Generic, NFData)

main = do
  let xs = map (* 2) [1..1000000] :: [Int]
  _ <- evaluate (force xs)         -- evaluates the whole list inside IO, here
  xs `deepseq` putStrLn "done"     -- a `deepseq` b: fully evaluate a, then return b
  r <- evaluate (rnf xs)           -- rnf :: a -> ()
  print (length xs)
```
Package: `deepseq`.

## Rules
- `NFData` class has `rnf :: a -> ()`. Derive with `Generic` plus `DeriveAnyClass`: `deriving (Generic, NFData)`.
- `evaluate $ force x` forces deep evaluation relative to other IO operations (the example in the `force` docs).
- `force x = x `deepseq` x`; `$!!` is the deep analogue of `$!`.
- `rwhnf` reduces a value to weak head normal form only.

## Gotchas
- Forcing a big structure repeatedly is O(n) every time; force once at the boundary.
- The `NFData (a -> b)` instance assumes WHNF equals NF for functions and is deprecated since deepseq-1.5.2.0.
- Handwritten `rnf` must force every field or you silently stay lazy; prefer the Generic default.
- `deepseq` on an infinite structure diverges.

## Self-check
- [ ] Every data type crossing a thread or timing boundary has an NFData instance.
- [ ] Timing of the forced value no longer includes evaluation in a later phase.

## Checked

2026-11-03. Confirmed against the Control.DeepSeq page: rnf, force, deepseq, $!!, rwhnf, Generic and DeriveAnyClass deriving, evaluate with force. Fixed: NFData for functions is deprecated since 1.5.2.0. Removed: bundling and build-depends claims, benchmark nf/whnf advice.
Method: documentation only; no commands were run.
