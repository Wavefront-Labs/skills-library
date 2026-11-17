---
id: computing-software.software-engineering.haskell.maybe-either-error-values
name: maybe-either-error-values
category: computing-software
field: software-engineering
product: haskell
tags: [haskell, maybe, either, error-handling, fromjust, either-monad, validation, note, maybe-function, maybe-either-error-values, haskell-errors]
level: intro
status: docs-checked
description: "Model failure with Maybe and Either, use maybe/either/fromMaybe, the Either monad and partitionEithers; avoid fromJust and head."
sources: ["https://hackage.haskell.org/package/base"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Maybe and Either for errors

**Goal:** return failures as values and compose them.

```haskell
import Data.Maybe (fromMaybe, mapMaybe, catMaybes, listToMaybe)
import Data.Either (lefts, rights, partitionEithers, either)

data ParseError = Empty | BadNum String deriving Show

parseAge :: String -> Either ParseError Int
parseAge "" = Left Empty
parseAge s = case reads s of [(n, "")] -> Right n; _ -> Left (BadNum s)

both :: Either ParseError (Int, Int)
both = do                       -- Either e is a Monad: stops at first Left
  a <- parseAge "3"
  b <- parseAge "x"
  pure (a, b)

fromMaybe 0 (lookup 'k' table)
mapMaybe parseMaybe inputs      -- parse and drop failures
partitionEithers results        -- ([errors],[successes])
either show (+1) (Right 2)
```

## Practices
- Use a domain error type, not `String`, so callers can match.
- `traverse f xs :: Either e [b]` fails fast at the first `Left`; to collect all errors, map over the items and use `partitionEithers`.
- `Maybe` for absence, `Either` for failure with reason, exceptions only for truly exceptional IO.
- `maybe`, `either`, `fromMaybe` replace trivial `case` expressions.

## Gotchas
- `fromJust`, `head` and `!!` are partial and throw on bad input; prefer `fromMaybe`, `listToMaybe` or pattern matching.
- `lefts`, `rights` and `partitionEithers` in `Data.Either` split a list of `Either` values.

## Self-check
- [ ] Parsers and lookups return Maybe/Either; no `fromJust` outside tests.
- [ ] Error types derive Show and Eq for testing.

## Checked

2026-11-03. Confirmed against base Data.Maybe and Data.Either pages: function names. Removed: validation package advice, HasCallStack claim, error remark.
Method: documentation only; no commands were run.
