---
id: computing-software.software-engineering.haskell.overloadedstrings-and-literals
name: overloadedstrings-and-literals
category: computing-software
field: software-engineering
product: haskell
tags: [haskell, overloadedstrings, isstring, numericunderscores, binaryliterals, overloadedlists, negativeliterals, overloadedstrings-and-literals]
level: practitioner
status: docs-checked
description: "Use OverloadedStrings with Text and ByteString, IsString, NumericUnderscores, BinaryLiterals and OverloadedLists, and fix the ambiguity errors they cause."
sources: ["https://downloads.haskell.org/ghc/latest/docs/users_guide/exts/overloaded_strings.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Literal-related extensions

**Goal:** write string and number literals for the right types.

```haskell
{-# LANGUAGE OverloadedStrings, NumericUnderscores, BinaryLiterals, OverloadedLists #-}
import qualified Data.Text as T
import Data.String (IsString(..))

greeting :: T.Text
greeting = "hello"                       -- fromString "hello" :: Text

newtype Name = Name String deriving Show
instance IsString Name where fromString = Name

million = 1_000_000 :: Int               -- NumericUnderscores
mask = 0b1010_1010 :: Int                -- BinaryLiterals
```

## Rules
- OverloadedStrings turns every string literal into `fromString "..."`; type `IsString a => a`.
- Literal patterns become equality tests, so the type needs `Eq` and `IsString`.
- OverloadedStrings extends defaulting: when all constraints are standard classes or `IsString`, `String` is tried last; supply `default (Int, Double, Text)` to default to another type.
- NumericUnderscores and BinaryLiterals are already part of GHC2021, so the pragma is only needed with older language editions.
- OverloadedLists does the same for list literals via `IsList`; useful for `Map` and `Set` literals but causes ambiguity with `length [1,2]` etc.
- `HexFloatLiterals` and `NegativeLiterals` exist; `NegativeLiterals` makes `-1` one token.

## Gotchas
- `putStrLn "x"` still works (String is IsString), but `length "abc"` can be ambiguous (Foldable t, IsString (t a)) because the defaulting rule above only fires when every constraint is a standard class or `IsString`; annotate or use `T.length`.
- `print "x"` is ambiguous with OverloadedStrings in GHCi unless defaulting finds String; `ExtendedDefaultRules` helps in GHCi.
- Using `printf` with OverloadedStrings can need a type annotation on the result (unconfirmed).
- Template: enable OverloadedStrings per module, not package wide, in libraries.

## Self-check
- [ ] Literals typed as Text/ByteString compile with no explicit `T.pack`.
- [ ] No ambiguous-type errors from `length`/`mapM_` on literals.

## Checked

2026-11-02. Confirmed against the GHC User's Guide exts/overloaded_strings and control pages: IsString, defaulting rule, pattern equality, GHC2021 literal extensions. Removed or fixed: printf claim softened.
Method: documentation only; no commands were run.
