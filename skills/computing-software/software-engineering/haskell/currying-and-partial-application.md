---
id: computing-software.software-engineering.haskell.currying-and-partial-application
name: currying-and-partial-application
category: computing-software
field: software-engineering
product: haskell
tags: [haskell, currying, partial-application, lambda, flip, uncurry, function-types, currying-and-partial-application, haskell-functions]
level: intro
status: docs-checked
description: "Understand that all Haskell functions take one argument, partially apply them, use flip/curry/uncurry, and read multi-arrow type signatures."
sources: ["https://www.haskell.org/onlinereport/haskell2010/haskellch3.html", "https://www.haskell.org/onlinereport/haskell2010/haskellch4.html", "https://www.haskell.org/onlinereport/haskell2010/haskellch9.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Currying and partial application

**Goal:** read `a -> b -> c` as `a -> (b -> c)` and build functions by supplying some arguments.

```haskell
add :: Int -> Int -> Int
add x y = x + y

inc :: Int -> Int
inc = add 1                    -- partial application; eta-reduced

map (add 10) [1,2,3]           -- [11,12,13]
zipWith (,) "ab" [1,2]         -- [('a',1),('b',2)]
flip (-) 1 10                  -- 9: flip swaps the first two arguments
uncurry add (3,4)              -- 7
curry fst 1 2                  -- 1
```

## Rules
- Function arrows associate to the right and application associates to the left: `f a b` is `(f a) b`, and
  `Int -> Int -> Float` means `Int -> (Int -> Float)`.
- A function that takes a tuple (`add (x,y)`) is not curried; prefer curried form for partial application.
- Argument order matters: put the argument most likely to be fixed first (configuration before data).
- Lambdas: `\x y -> x + y`; `\_ -> 0`.
- `curry f x y = f (x, y)`, `uncurry f p = f (fst p) (snd p)` and `flip f x y = f y x` are Prelude functions.

## Gotchas
- Constructors partially apply too: `map Just xs`.
- Over-eager eta reduction can hit the monomorphism restriction: a simple pattern binding such as `plus = (+)` with no
  signature is not generalised over its class constraint, and defaulting may then pick `Integer`. Add a type signature.
- A "no instance for Show" error on a function type usually means you forgot an argument and tried to print a function.

## Self-check
- [ ] Top-level point-free definitions have explicit signatures.

## Checked

2026-11-08. Confirmed against the Haskell 2010 Report (section 4.1.2 function arrows associate to the right, section 3.3 application associates to the left and constructors partially apply, section 4.5.5 monomorphism restriction and defaulting, Prelude definitions of `flip`, `curry`, `uncurry`). Removed: the `Data.Map.insert` argument-order example, the exact GHC error text and the GHCi `:t` self-check (not in the pages read).
Method: documentation only; no commands were run.
