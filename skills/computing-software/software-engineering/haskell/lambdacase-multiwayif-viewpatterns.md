---
id: computing-software.software-engineering.haskell.lambdacase-multiwayif-viewpatterns
name: lambdacase-multiwayif-viewpatterns
category: computing-software
field: software-engineering
product: haskell
tags: [haskell, lambdacase, multiwayif, viewpatterns, patternsynonyms, tuplesections, extensions, lambdacase-multiwayif-viewpatterns]
level: practitioner
status: docs-checked
description: "Use the syntax extensions LambdaCase, MultiWayIf, ViewPatterns, TupleSections and PatternSynonyms and know when each is clearer than plain Haskell 2010."
sources: ["https://www.haskell.org/onlinereport/haskell2010/", "https://downloads.haskell.org/ghc/latest/docs/users_guide/exts/lambda_case.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# LambdaCase, MultiWayIf, ViewPatterns and friends

**Goal:** apply the common syntax extensions where they shorten code without obscuring it. Enable per file with
`{-# LANGUAGE ... #-}`.

```haskell
{-# LANGUAGE LambdaCase, MultiWayIf, ViewPatterns, TupleSections #-}

toNum :: String -> Int
toNum = \case                       -- LambdaCase: \x -> case x of
  "one" -> 1
  "two" -> 2
  _     -> 0

sign :: Int -> String
sign n = if | n < 0 -> "neg"        -- MultiWayIf: guards inside an expression
            | n == 0 -> "zero"
            | otherwise -> "pos"

firstWord :: String -> String
firstWord (words -> (w:_)) = w      -- ViewPatterns: apply a function, then match
firstWord _ = ""

pairs = map (,True) [1,2,3]         -- TupleSections: [(1,True),(2,True),(3,True)]
```
`\cases` (multi-argument lambda case) exists since GHC 9.4.1.

## PatternSynonyms
`pattern Zero :: Int; pattern Zero = 0` gives a named pattern: bidirectional with `=`, one-way matching with `<-`.
Export it with `pattern Zero` in the export list; add a `{-# COMPLETE ... #-}` pragma so the checker sees exhaustiveness.

## Gotchas
- MultiWayIf guards use layout; mis-indented alternatives give confusing parse errors.
- ViewPatterns functions run on every match attempt; keep them cheap and pure.
- None of these are Haskell 2010. GHC2021 enables TupleSections but not LambdaCase, MultiWayIf or ViewPatterns; GHC2024 (GHC 9.10.1 or later) adds LambdaCase.

## Self-check
- [ ] File compiles only after the pragma is present (remove it to see the error).
- [ ] Each extension removes a named helper or nested case; otherwise do not use it.

## Checked

2026-11-02. Confirmed against the GHC User's Guide exts/lambda_case, multiway_if, view_patterns and control pages: \cases since 9.4.1, edition membership. Removed or fixed: unconfirmed hedges.
Method: documentation only; no commands were run.
