---
id: computing-software.software-engineering.haskell.eq-ord-show-read
name: eq-ord-show-read
category: computing-software
field: software-engineering
product: haskell
tags: [haskell, eq, ord, show, read, showsprec, compare, reads, readmaybe, eq-ord-show-read, haskell-stdclasses]
level: intro
status: draft
description: "Use Eq, Ord, Show and Read correctly, derived vs hand-written, showsPrec, compare, comparing, and safe parsing with Text.Read.readMaybe."
sources: ["https://hackage.haskell.org/package/base", "https://www.haskell.org/onlinereport/haskell2010/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Eq, Ord, Show and Read

**Goal:** write correct instances and parse safely.

```haskell
import Text.Read (readMaybe)
import Data.Ord (comparing, Down(..))
import Data.List (sortBy, sortOn)

data P = P Int String deriving (Eq, Ord, Show, Read)

readMaybe "42" :: Maybe Int          -- Just 42; read "x" would throw
readMaybe "P 1 \"a\"" :: Maybe P     -- derived Read parses derived Show output
sortOn Down [1,3,2]                  -- [3,2,1]
compare 1 2                          -- LT
max "a" "b"

instance Show Temp where
  showsPrec d (Temp t) = showParen (d > 10) $ showString "Temp " . showsPrec 11 t
```

## Laws
- `Eq`: reflexive, symmetric, transitive. Floating `NaN /= NaN` breaks reflexivity.
- `Ord`: total order consistent with `Eq`; define `compare` or `<=` (MINIMAL).
- `show` should be valid Haskell where possible and `read . show == id` for derived instances.
  For user-facing text, write a separate `pretty` function and keep `Show` for debugging.

## Gotchas
- Never use `read` on user input; use `readMaybe`.
- Show for `String` escapes characters (`show "a\n"` is `"\"a\\n\""`); use `putStrLn` for display.
- Show for Double uses shortest representation; use `Numeric.showFFloat (Just 2) x ""` for fixed decimals.
- Comparing Doubles with `==` is fragile; use a tolerance.
- Records derived Show prints `P {a = 1}`; that is machine, not user, format.

## Self-check
- [ ] `readMaybe` used for all external input.
- [ ] Property: `compare x y == compare y x` flipped (QuickCheck can verify).
