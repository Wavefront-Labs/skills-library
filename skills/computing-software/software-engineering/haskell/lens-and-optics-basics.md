---
id: computing-software.software-engineering.haskell.lens-and-optics-basics
name: lens-and-optics-basics
category: computing-software
field: software-engineering
product: haskell
tags: [haskell, lens, optics, traversal, prism, iso, view, over, set, microlens, generic-lens, makelenses, van-laarhoven, lens-and-optics-basics, haskell-optics]
level: advanced
status: draft
description: "Use lens or optics for nested records: makeLenses, view/set/over operators, traversals and prisms, and the lens vs microlens vs optics tradeoffs."
sources: ["https://hackage.haskell.org/package//lens", "https://hackage.haskell.org/package//optics"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Lenses and optics

**Goal:** read and update deeply nested data without boilerplate.

```haskell
{-# LANGUAGE TemplateHaskell #-}
import Control.Lens

data Addr = Addr { _city :: String, _zip :: Int } deriving Show
data Person = Person { _name :: String, _addr :: Addr, _tags :: [String] } deriving Show
makeLenses ''Addr
makeLenses ''Person

p = Person "ann" (Addr "Perth" 6000) ["a","b"]
p ^. addr . city                           -- "Perth"      view
p & addr . city .~ "Sydney"                -- set
p & addr . zip %~ (+ 1)                    -- over (modify)
p & tags . traverse %~ map toUpper         -- traversal: all elements
p ^.. tags . traverse                      -- toListOf
p ^? tags . ix 5                           -- Maybe (safe index)
_Just # 3                                  -- prism construction: Just 3
over _1 (+1) (1, 2)
```

## Concepts
- Lens: exactly one focus (get/set). Traversal: zero or more. Prism: sum constructor (preview/review). Iso: reversible conversion. Fold/Getter: read only.
- They compose with plain `.` (van Laarhoven representation), left to right in reading order.
- Operators: `^.` view, `.~` set, `%~` over, `&` pipeline, `^?` first, `^..` all, `<>~`, `+~`, `use`/`.=`/`%=` in `State`.
- Libraries: `lens` (richest, large dependency set), `microlens` (small), `optics` (abstract interface with better error messages, `makeFieldLabelsNoPrefix`, OverloadedLabels), `generic-lens` (derive via Generic: `p ^. field @"name"`), and OverloadedRecordDot for plain reads.

## Gotchas
- `makeLenses` needs underscore-prefixed fields and TH (staging restriction: declaration order matters; put `makeLenses` after the types and before use).
- Error messages for operator misuse are cryptic; add type signatures.
- Heavy operator use hurts onboarding; pick one optics library per project.
- `lens` increases compile times; consider `microlens` for libraries.

## Self-check
- [ ] A nested update that took record-update boilerplate is a one-line lens.
- [ ] Optics library choice documented.
