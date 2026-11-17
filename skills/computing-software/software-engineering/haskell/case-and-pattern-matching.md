---
id: computing-software.software-engineering.haskell.case-and-pattern-matching
name: case-and-pattern-matching
category: computing-software
field: software-engineering
product: haskell
tags: [haskell, case, pattern-matching, as-patterns, irrefutable-patterns, wildcard, incomplete-patterns, case-and-pattern-matching]
level: intro
status: docs-checked
description: "Pattern match on constructors, literals, tuples, lists, as-patterns and irrefutable patterns, with exhaustiveness checking by -Wincomplete-patterns."
sources: ["https://www.haskell.org/onlinereport/haskell2010/haskellch3.html", "https://www.haskell.org/onlinereport/haskell2010/haskellch4.html", "https://downloads.haskell.org/ghc/latest/docs/users_guide/using-warnings.html", "https://downloads.haskell.org/ghc/latest/docs/users_guide/exts/strict.html", "https://downloads.haskell.org/ghc/latest/docs/users_guide/exts/overloaded_strings.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Case expressions and pattern matching

**Goal:** write total, ordered pattern matches the compiler can check.

```haskell
data Shape = Circle Double | Rect Double Double

area :: Shape -> Double
area (Circle r) = pi * r * r
area (Rect w h) = w * h

describe :: [Int] -> String
describe xs = case xs of
  []        -> "empty"
  [x]       -> "one: " ++ show x
  all'@(x:_) -> "starts with " ++ show x ++ " of " ++ show (length all')   -- as-pattern
```

## Pattern forms
Constructor patterns, literals (`0`, `'a'`, `"str"`), tuples, list syntax `[a,b]`, cons `(x:xs)`, wildcard `_`,
as-pattern `name@pat`, bang pattern `!x` (BangPatterns), irrefutable `~(a,b)` (lazy, never fails at match time).

## Rules
- Equations and alternatives are tried top to bottom; first match wins. If every guarded alternative fails, matching
  continues with the next alternative; if none succeeds the result is bottom.
- Matching a constructor pattern against a diverging value diverges. A `~` pattern always succeeds and defers the
  match until one of its variables is used.
- Nested patterns are fine: `f (Just (x:_)) = x`.
- `let (a, b) = pair` is a lazy pattern binding (an implicit `~`); it does not fail until a or b is used.

## Failure modes
- Incomplete patterns compile but can fail at run time. `-Wincomplete-patterns` warns (it is switched on by `-W`,
  so `-Wall` includes it); `-Werror=incomplete-patterns` makes that warning fatal.
- Overlapping or unreachable equations are reported by `-Woverlapping-patterns`, which is on by default.
- Matching string literals under OverloadedStrings becomes an equality test, so the scrutinee type needs `Eq` (and `IsString`).

## Self-check
- [ ] Add a new constructor and confirm GHC warns at every match site.
- [ ] No wildcard `_` in a match that should enumerate all constructors (it hides future cases).

## Checked

2026-11-08. Confirmed against the Haskell 2010 Report (section 3.17 pattern matching semantics, section 3.13 case alternatives, section 4.4.3 pattern bindings as irrefutable) and the GHC User's Guide: `-Wincomplete-patterns` (switched on by -W, included in -Wall), `-Woverlapping-patterns` (on by default), `-Werror=<flag>`, BangPatterns, and OverloadedStrings equality-test desugaring. Removed: the n+k removal note, the WHNF wording and the quoted run-time message (not confirmed in the pages read).
Method: documentation only; no commands were run.
