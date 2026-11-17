---
id: computing-software.software-engineering.haskell.inlining-specialisation-pragmas
name: inlining-specialisation-pragmas
category: computing-software
field: software-engineering
product: haskell
tags: [haskell, inline, noinline, inlinable, specialize, rules, unpack, strictness, pragma, worker-wrapper, inlining-specialisation-pragmas]
level: advanced
status: docs-checked
description: "Use INLINE, NOINLINE, INLINABLE, SPECIALIZE, UNPACK and RULES pragmas appropriately to remove dictionary passing and enable fusion."
sources: ["https://downloads.haskell.org/ghc/latest/docs/users_guide/exts/pragmas.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Inlining and specialisation

**Goal:** guide GHC's optimiser on hot code without guessing.

```haskell
{-# INLINE add #-}                         -- always inline at saturated call sites
add :: Int -> Int -> Int
add = (+)

{-# INLINABLE sumBy #-}                    -- expose unfolding so callers can specialise
sumBy :: Num a => (b -> a) -> [b] -> a

{-# SPECIALIZE sumBy :: (b -> Int) -> [b] -> Int #-}   -- generate an Int version

{-# NOINLINE counter #-}                    -- needed for a global unsafePerformIO IORef
counter :: IORef Int
counter = unsafePerformIO (newIORef 0)

data P = P {-# UNPACK #-} !Int {-# UNPACK #-} !Int

{-# RULES "map/map" forall f g xs. map f (map g xs) = map (f . g) xs #-}
{-# INLINE [1] f #-}                        -- phase control: inline in phase 1 and later
```

## Rules
- Overloaded functions (`Num a =>`) pass dictionaries at run time unless specialised. Inside a module GHC specialises automatically with `-O`; across modules, mark `INLINABLE` or use `-fspecialise-aggressively`.
- Recursive groups are cut by loop breakers that are never inlined; GHC avoids choosing an INLINE function as the breaker but sometimes must, so INLINE on a recursive function is unreliable: use a local worker loop. INLINABLE is fine on recursive functions.
- Over-inlining bloats code and compile time; use for small wrappers and combinators.
- RULES fire only when optimising and only in matching phases; they must preserve semantics. Check with `-ddump-rule-firings`.
- Useful dumps: `-ddump-simpl -dsuppress-all -dsuppress-uniques` (Core), `-ddump-inlinings`, `-ddump-stg-final`.

## Gotchas
- A function that is exported with INLINE adds its body to the interface file: API change for downstream compile times.
- `unsafePerformIO` globals need `NOINLINE` or duplicates appear.
- Strict accumulators plus INLINE of combinators are the usual cause of "fusion" success; verify in Core.
- Specialising for too many types explodes code size.

## Self-check
- [ ] Core dump of the hot loop shows no dictionary arguments or boxed Ints.
- [ ] Benchmark shows the pragma helped.

## Checked

2026-11-02. Confirmed against the GHC User's Guide exts/pragmas and debugging pages: INLINE/INLINABLE/SPECIALIZE semantics, loop breakers, dump flags. Removed or fixed: -ddump-spec, INLINE-on-recursive claim.
Method: documentation only; no commands were run.
