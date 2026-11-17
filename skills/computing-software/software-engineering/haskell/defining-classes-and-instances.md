---
id: computing-software.software-engineering.haskell.defining-classes-and-instances
name: defining-classes-and-instances
category: computing-software
field: software-engineering
product: haskell
tags: [haskell, typeclass, class-declaration, instance, default-methods, minimal-pragma, flexibleinstances, multiparamtypeclasses, defining-classes-and-instances, haskell-typeclasses]
level: practitioner
status: draft
description: "Declare classes with default methods and MINIMAL pragmas, write instances, superclasses, and know FlexibleInstances, FlexibleContexts and MultiParamTypeClasses."
sources: ["https://www.haskell.org/onlinereport/haskell2010/", "https://downloads.haskell.org/ghc/latest/docs/users_guide/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Defining classes and instances

**Goal:** design a class interface with defaults and write coherent instances.

```haskell
class Shape a where
  area      :: a -> Double
  perimeter :: a -> Double
  describe  :: a -> String
  describe x = "area " ++ show (area x)        -- default method
  {-# MINIMAL area, perimeter #-}

data Circle = Circle Double
instance Shape Circle where
  area (Circle r) = pi * r * r
  perimeter (Circle r) = 2 * pi * r

class Eq a => Container f a where ...           -- superclass context (needs MultiParamTypeClasses)
instance Show a => Show (Tree a) where          -- instance with context
  show = ...
```

## Rules
- Instances are global and unique per (class, type head): "orphan" instances (neither class nor type defined
  in the module) risk duplicates; `-Worphans` warns.
- Haskell 2010 requires instance heads like `T a b` with distinct variables; `FlexibleInstances` allows
  `instance C [Char]` and `instance C (Maybe Int)`. `FlexibleContexts` allows non-variable contexts.
  Both are on in GHC2021.
- `MultiParamTypeClasses` allows `class C a b`; resolve ambiguity with `FunctionalDependencies`
  (`class C a b | a -> b`) or type families.
- `-Wmissing-methods` (on by default) reports unimplemented methods not covered by MINIMAL.
- Overlapping instances need `{-# OVERLAPPING #-}`/`{-# OVERLAPPABLE #-}` pragmas on the instances.

## Gotchas
- A class method with no mention of the class variable in its type is ambiguous and rejected unless AllowAmbiguousTypes.
- Passing dictionaries has a cost; `INLINABLE`/`SPECIALIZE` removes it in hot paths.
- Do not write instances like `instance Num a => Show a`: they overlap with everything.

## Self-check
- [ ] Each new instance has all MINIMAL methods, with no `-Wmissing-methods`.
- [ ] Instances live in the module of the class or the type, not in a third module.
