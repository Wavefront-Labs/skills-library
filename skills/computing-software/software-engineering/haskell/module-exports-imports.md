---
id: computing-software.software-engineering.haskell.module-exports-imports
name: module-exports-imports
category: computing-software
field: software-engineering
product: haskell
tags: [haskell, module, export-list, import-qualified, hiding, as-alias, reexport, prelude, abstract-types, module-exports-imports, haskell-modules]
level: intro
status: docs-checked
description: "Structure modules with export lists, abstract types, qualified and hiding imports, re-exports, implicit Prelude and the Main module rules."
sources: ["https://www.haskell.org/onlinereport/haskell2010/haskellch5.html", "https://downloads.haskell.org/ghc/latest/docs/users_guide/using-warnings.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Modules, exports and imports

**Goal:** organise code with clear interfaces.

```haskell
module Data.Stack
  ( Stack          -- abstract: constructors hidden
  , empty, push, pop
  , module Data.Maybe   -- re-export
  ) where

import qualified Data.Map.Strict as M     -- use M.lookup
import Data.List (sortOn, foldl')          -- explicit list
import Data.Char hiding (isSpace)          -- everything but isSpace
import Prelude hiding (lookup)
import Data.Stack as Stk                   -- brings names in unqualified AND as Stk.name
```

## Rules
- A program is modules, one of which must be called `Main` and export `main`, a computation of type `IO t` for some `t`.
- Export list items: `T` (type only), `T(..)` (all constructors and fields in scope), `T(A,B)`, functions, `module M`.
  Omitting the list exports every entity defined in the module (not imported ones): avoid in libraries.
- Qualified names need the alias: `M.lookup`.
- Export lists are cumulative (the union of the items), and an entity can only be exported if the module declares or imports it.
- Instances cannot be named in import or export lists: all instances in scope are always exported, and any import brings in all instances of the imported module.

## Practices
- Import data structures qualified (`Map`, `Set`, `Text`, `ByteString`), list functions explicitly.
- Keep an `Internal` module exposing constructors for tests, and a public module with the abstract API.
- `-Wunused-imports` is in `-Wall`; `-Wmissing-export-lists` is a separate flag that warns on a module with no explicit export list.

## Gotchas
- A name clash is an error only where the ambiguous name is used ("ambiguous"); qualify the reference to resolve it.
- `import Foo ()` imports no names but brings in the instances visible in `Foo`; `-Wunused-imports` never reports it.
- Exporting a type as `T` without its constructors keeps the type abstract.
- Separate compilation of mutually recursive modules is implementation dependent: the report does not define the details.

## Self-check
- [ ] `ghc -Wall` has no unused imports.
- [ ] Public API of each library module listed explicitly.

## Checked

2026-11-08. Confirmed against the Haskell 2010 Report chapter 5 (Main and `IO t`, export list forms and cumulative lists, import forms including `hiding`, `qualified`, `as` and `import A()`, instance import and export, ambiguity only on use, abstract data types, separate compilation of mutually recursive modules) and the GHC warnings page for `-Wunused-imports`, `-Wmissing-export-lists` and `-Wall` membership. Removed: the `Data/Stack.hs` file-name note, `ImportQualifiedPost` line, `ghc -main-is`, `.hs-boot`, the circular-import absolute claim and the `Map.\\` operator example.
Method: documentation only; no commands were run.
