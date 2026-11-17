---
id: computing-software.software-engineering.haskell.comments-and-pragmas
name: comments-and-pragmas
category: computing-software
field: software-engineering
product: haskell
tags: [haskell, comments, haddock-comments, literate-haskell, pragmas, lhs, unlit, comments-and-pragmas]
level: intro
status: docs-checked
description: "Write line, block and Haddock comments, use literate Haskell .lhs files with bird tracks, and the pragma forms LANGUAGE, OPTIONS_GHC, INLINE and SPECIALIZE."
sources: ["https://www.haskell.org/onlinereport/haskell2010/", "https://downloads.haskell.org/ghc/latest/docs/users_guide/exts/pragmas.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Comments, literate Haskell and pragmas

**Goal:** know which comment forms exist and where each pragma is legal.

## Comment forms
```haskell
-- line comment (the dashes must not be part of an operator: --> is an operator)
{- block comment {- nested comments are allowed -} -}
-- | Haddock doc for the next declaration
-- ^ Haddock doc for the previous item (argument or constructor field)
```
`--|` without a space is an operator, not a comment. Block comments nest.

## Literate Haskell
(Literate rules are from the Haskell 2010 Report, chapter 10; unconfirmed here.) Files ending `.lhs` treat text as comments; code is either "bird tracks" (lines starting `> `) or
`\begin{code} ... \end{code}` blocks. Code must be separated from prose by a blank line. GHC unlits them
automatically, so `ghc File.lhs` and `:l File.lhs` in GHCi just work.

## Pragmas
- File header (before `module`): `{-# LANGUAGE LambdaCase, TupleSections #-}`, `{-# OPTIONS_GHC -Wall #-}`.
- Declaration pragmas: `{-# INLINE f #-}`, `{-# NOINLINE f #-}`, `{-# INLINABLE f #-}`,
  `{-# SPECIALIZE f :: Int -> Int #-}`, `{-# DEPRECATED f "use g" #-}`, `{-# MINIMAL (==) | (/=) #-}` in a class.
- Unknown pragmas are ignored (`-Wunrecognised-pragmas`); a misspelled `LANGUAGE` extension is an error.

## Gotchas
- `LANGUAGE` pragmas after `module` are ignored with a warning; they must come first (comments may precede).
- Haddock: `-- |` before a data constructor documents it; `-- ^` after a field documents the field.
- Unbalanced `{-` in a comment swallows the rest of the file because block comments nest.
- `OPTIONS_GHC` flags that change the build model (like `-threaded`) belong in the cabal file, not a pragma.

## Self-check
- [ ] `ghc -Wall` shows no `-Wmisplaced-pragmas`.
- [ ] `.lhs` blank-line rule observed; file loads in GHCi with `:l File.lhs`.

## Checked

2026-11-02. Confirmed against the GHC User's Guide exts/pragmas and using-warnings pages: pragma forms, -Wunrecognised-pragmas, -Wmisplaced-pragmas. Removed or fixed: literate-Haskell rules left as report-based, flagged.
Method: documentation only; no commands were run.
