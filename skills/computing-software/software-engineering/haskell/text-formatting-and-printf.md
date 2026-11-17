---
id: computing-software.software-engineering.haskell.text-formatting-and-printf
name: text-formatting-and-printf
category: computing-software
field: software-engineering
product: haskell
tags: [haskell, printf, text-printf, formatting, showfloat, numeric, showhex, builder, text-formatting-and-printf]
level: practitioner
status: docs-checked
description: "Format numbers and strings with Text.Printf.printf and Numeric.showFFloat/showHex/readHex, with the printf type pitfalls."
sources: ["https://hackage.haskell.org/package//text"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Formatting text and numbers

**Goal:** produce fixed-format output without hand-rolled padding.

```haskell
import Text.Printf (printf, hPrintf)
import Numeric (showHex, showFFloat, showOct, readHex)
import Text.Printf (printf)

printf "%5d|%-5d|%05d\n" (42 :: Int) (42 :: Int) (42 :: Int)
printf "%.2f %s %c %x\n" (3.14159 :: Double) "str" 'z' (255 :: Int)
s <- pure (printf "%d-%d" (1 :: Int) (2 :: Int) :: String)   -- printf can return String
showFFloat (Just 2) 3.14159 ""        -- "3.14"
showHex (255 :: Int) ""                -- "ff"
fst (head (readHex "ff")) :: Int       -- 255
hPrintf stderr "warn %s\n" "x"
```

## Notes
- `printf` is variadic via type classes; the return value is either a `String` or an `IO` action. Annotate numeric literal arguments (`(42 :: Int)`) so their type is not left to defaulting.
- A mismatch between the arguments and the format string throws an exception at run time.
- `printf` can be extended to other types by instantiating `PrintfArg` and providing `formatArg`.
- `Data.Text.Lazy.Builder` and `Data.ByteString.Builder` provide Builders for assembling larger output.

## Gotchas
- `%s` takes a `String`; convert other values first (for example with `show`, or `T.unpack` for `Text`).
- `showFFloat (Just 2) x ""` gives fixed notation with 2 decimals.
- `round` returns the even integer when exactly between two integers; check edge cases before relying on it for display.

## Self-check
- [ ] Each printf line has been exercised once so mismatches surface early.

## Checked

2026-11-03. Confirmed against base Text.Printf and Numeric pages: printf return types, runtime exception on mismatch, PrintfArg extension, showFFloat/showHex/readHex. Removed: fmt/formatting/text-show claims, Data.Text.Format history, Text instance claim, rounding comparison.
Method: documentation only; no commands were run.
