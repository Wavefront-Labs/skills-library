---
id: computing-software.software-engineering.haskell.template-haskell-basics
name: template-haskell-basics
category: computing-software
field: software-engineering
product: haskell
tags: [haskell, template-haskell, splice, quasiquote, th, declaration-quotes, reify, typed-th, makelenses, staging-restriction, template-haskell-basics]
level: sme
status: docs-checked
description: "Use Template Haskell: expression/declaration quotes and splices, reify, QuasiQuotes, typed TH, the stage restriction, and compile-time cost."
sources: ["https://downloads.haskell.org/ghc/latest/docs/users_guide/exts/template_haskell.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Template Haskell

**Goal:** generate code at compile time, with discipline. Package: `template-haskell` (boot library).

```haskell
{-# LANGUAGE TemplateHaskell, QuasiQuotes #-}
-- TH.hs
import Language.Haskell.TH
power :: Int -> Q Exp                       -- Q is the compile-time monad
power 0 = [| const 1 |]
power n = [| \x -> x * $(power (n - 1)) x |]

mkGetters :: Name -> Q [Dec]
mkGetters ty = do
  TyConI (DataD _ _ _ _ [RecC _ fields] _) <- reify ty      -- inspect a type
  concat <$> mapM (\(f, _, t) -> do
     let g = mkName ("get_" ++ nameBase f)
     pure [FunD g [Clause [] (NormalB (VarE f)) []]]) fields

-- Main.hs (a different module!)
cube = $(power 3)                           -- expression splice, run at compile time
$(mkGetters ''Person)                       -- declaration splice; ''Type names a type, 'val a value
```
Quasiquoters: `[json| {"a": 1} |]` use a `QuasiQuoter { quoteExp = ... }`; typed TH uses `Code Q a` and `[|| ... ||]`/`$$( )`.

## Rules
- Levels and stages: code in a top-level splice runs at compile time, so it may use imported identifiers but not same-module top-level definitions (see "Levels and Stages" in the User's Guide).
- Top-level declaration splices break the file into declaration groups; each group is type-checked in order, so earlier groups cannot see later ones.
- `lift`/`Lift` (DeriveLift) moves values into code; `runIO` can read files (use `addDependentFile`, documented in the template-haskell package on Hackage, so builds notice changes).
- Common uses: lens generation, embedding files (`file-embed`), compile-time validated literals, boilerplate instances.

## Gotchas
- Compile time, cross-compilation (needs external interpreter) and tooling (HLS memory) suffer; prefer Generics, DerivingVia, or plain code when possible.
- TH runs arbitrary code with the compiler's privileges: audit TH libraries.
- Profiling builds require dynamic/profiling object consistency.

## Self-check
- [ ] The splice has an ordinary-code alternative considered and rejected for a reason.
- [ ] `addDependentFile` used for external inputs.

## Checked

2026-11-02. Confirmed against the GHC User's Guide exts/template_haskell page: declaration groups, levels and stages, TemplateHaskellQuotes. Removed or fixed: stage restriction wording replaced.
Method: documentation only; no commands were run.
