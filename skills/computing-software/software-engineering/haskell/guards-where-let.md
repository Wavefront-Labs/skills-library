---
id: computing-software.software-engineering.haskell.guards-where-let
name: guards-where-let
category: computing-software
field: software-engineering
product: haskell
tags: [haskell, guards, where, let-in, otherwise, pattern-guards, guards-where-let, haskell-expressions]
level: intro
status: docs-checked
description: "Use guards, where and let in function definitions, pattern guards, and scoping rules so that definitions read top-down."
sources: ["https://www.haskell.org/onlinereport/haskell2010/haskellch3.html", "https://www.haskell.org/onlinereport/haskell2010/haskellch9.html", "https://downloads.haskell.org/ghc/latest/docs/users_guide/using-warnings.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Guards, where and let

**Goal:** choose between guards, `if`, `case`, `where` and `let` for readable definitions.

```haskell
classify :: Int -> String
classify n
  | n < 0     = "negative"
  | n == 0    = "zero"
  | isBig     = "big"
  | otherwise = "small"
  where isBig = n > 1000          -- visible in ALL guards of this equation

-- pattern guard: bind with <- inside a guard
lookupAge :: String -> [(String,Int)] -> String
lookupAge k env
  | Just a <- lookup k env, a >= 18 = "adult"
  | otherwise = "unknown or minor"
```

## let vs where
- `let ... in expr` is an expression and can appear inside other expressions and in `do` blocks.
- `where` attaches to an equation (or a `case` alternative) and scopes over all of its guards and bodies; it cannot be used
  inside an expression.
- Both are mutually recursive (letrec semantics).

## Details
- `otherwise` is just `True`.
- If all guards of an equation fail, matching falls through to the next equation.
- A boolean guard `g` is equivalent to the pattern guard `True <- g`.

## Failure modes
- A missing `otherwise` leaves the function partial: if no guard succeeds in any equation the result is bottom.
- Shadowing: an inner `x` hides an outer `x`; `-Wname-shadowing` (in `-Wall`) warns, and it ignores names starting with an underscore.
- Using `where` helpers that capture arguments makes them hard to test; lift them to top level when reusable.

## Self-check
- [ ] `-Wall` is clean: no incomplete patterns, no shadowing.
- [ ] Each helper used by more than one guard lives in `where`, not repeated.

## Checked

2026-11-08. Confirmed against the Haskell 2010 Report (section 3.13 case expressions and guards: pattern guards, boolean guards, where scope, fall-through to the next alternative; section 3.12 let as letrec; section 3.14 do with let; Prelude `otherwise = True`) and the GHC warnings page for `-Wname-shadowing` and `-Wall` (includes `-Wincomplete-patterns` via `-Wextra`). Removed: the MonoLocalBinds line (not confirmed in the pages read).
Method: documentation only; no commands were run.
