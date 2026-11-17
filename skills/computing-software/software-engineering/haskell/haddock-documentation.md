---
id: computing-software.software-engineering.haskell.haddock-documentation
name: haddock-documentation
category: computing-software
field: software-engineering
product: haskell
tags: [haskell, haddock, doc-comments, haddock-markup, cabal-haddock, hyperlinks, module-header, doctest-examples, prologue, haddock-documentation, haskell-documentation]
level: practitioner
status: docs-checked
description: "Document Haskell code with Haddock: comment forms, markup (code blocks, links, headings), module headers and the cabal haddock commands."
sources: ["https://haskell-haddock.readthedocs.io/latest/markup.html", "https://cabal.readthedocs.io/en/stable/cabal-commands.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Haddock

**Goal:** API documentation that builds locally and on Hackage.

```haskell
{-|
Module      : Data.Stack
Description : A simple stack.
Copyright   : (c) You, 2026
License     : BSD-3-Clause
Maintainer  : you@example.com

Longer description with @code@, /emphasis/, __bold__, and links to 'push' and "Data.Map".
-}
module Data.Stack
  ( -- * Types
    Stack
    -- * Operations
  , push   -- ^ push onto the stack
  , pop
  ) where

-- | A last-in first-out collection.
data Stack a
  = Empty                 -- ^ no elements
  | Cons a (Stack a)      -- ^ head and rest

-- | Push an element.
--
-- >>> toList (push 1 Empty)
-- [1]
push :: a -- ^ the element
     -> Stack a -- ^ the stack
     -> Stack a
```

## Markup cheat sheet
`'name'` links an identifier; `"Module.Name"` links a module; `@code@` is inline monospace; `/emphasis/` and `__bold__`; a paragraph wrapped in `@...@` or lines starting with `>` ("bird tracks") are code blocks; `* item` bullets; `(1)` or `1.` numbered items; `-- * Heading` and `-- ** Subheading` section headings; `-- $name` named chunks of documentation; `>>> expr` followed by result lines is an interactive example. Put a blank line before a list or it renders inline.

## Commands
```bash
cabal haddock                  # build Haddock documentation for the targets
cabal haddock-project          # HTML for all local packages, default output ./haddocks (--output to change)
```
`-Wmissing-export-lists` is a GHC warning for modules with no explicit export list.

## Gotchas
- A `-- |` placed before a type signature documents the function; `-- ^` after an argument documents that argument.
- Unqualified identifier links work only if the name is in scope in that module.
- Haddock lists only exported entities, in export-list order; export list headings (`-- *`) shape the page. With no export list, all entities defined by the module are exported and section headings go in the module body.
- Module header fields are optional but must appear in order; continuation lines must be indented more than their label.

## Self-check
- [ ] `cabal haddock` completes and every export has documentation.
- [ ] Example lines (`>>>`) show the real result.

## Checked

2026-11-08. Confirmed against the Haddock Documentation and Markup page: `-- |` and `-- ^` annotations, identifier and module links, emphasis, bold, monospace, code blocks (`@...@` and bird tracks), list syntax, `>>>` examples, section headings, named chunks, export-list ordering, module description field order; and the Cabal commands page for `cabal haddock` and `cabal haddock-project` (default `./haddocks`, `--output`); `-Wmissing-export-lists` on the GHC warnings page. Removed: the `--haddock-all`, `--haddock-hyperlink-source`, `--haddock-for-hackage`, standalone `haddock --html --odir` and `-haddock`/`-Winvalid-haddock` claims, `=` header headings, `<url label>` links, `-- $setup` doctest blocks and the hidden-dependency gotcha (none confirmed in the pages read).
Method: documentation only; no commands were run.
