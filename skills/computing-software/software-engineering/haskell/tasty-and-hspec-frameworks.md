---
id: computing-software.software-engineering.haskell.tasty-and-hspec-frameworks
name: tasty-and-hspec-frameworks
category: computing-software
field: software-engineering
product: haskell
tags: [haskell, tasty, hspec, tasty-discover, hspec-discover, testgroup, test-suite, golden-tests, tasty-golden, tasty-quickcheck, tasty-and-hspec-frameworks]
level: practitioner
status: docs-checked
description: "Organise tests with Tasty (testGroup, -p patterns, golden tests) or Hspec (describe/it, expectations, --match, hspec-discover) in an exitcode-stdio test-suite."
sources: ["https://hackage.haskell.org/package/tasty", "https://hackage.haskell.org/package/tasty-golden", "https://hspec.github.io/", "https://hspec.github.io/hspec-discover.html", "https://hspec.github.io/expectations.html", "https://hspec.github.io/match.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tasty and Hspec

**Goal:** a test tree, filtering and good reports, hooked to `cabal test`.

## Tasty
```haskell
import Test.Tasty
import Test.Tasty.HUnit
import Test.Tasty.QuickCheck as QC
import Test.Tasty.Golden (goldenVsString)

main = defaultMain $ testGroup "all"
  [ testCase "unit" (1 + 1 @?= (2 :: Int))
  , QC.testProperty "reverse" (\xs -> reverse (reverse xs) == (xs :: [Int]))
  , goldenVsString "render" "test/golden/out.txt" (pure (renderBS doc))
  ]
```
Run the test program with `-p PATTERN` (a pattern is an awk expression; a plain word such as `-p reverse` selects tests with that word in their name or group), `-j`/`--num-threads`, and `--accept` to update golden files (tasty-golden). `tasty-discover` is listed on the Tasty page for test discovery.

## Hspec
```haskell
import Test.Hspec
main = hspec $ describe "parse" $ do
  it "reads ints" $ parse "42" `shouldBe` Right 42
  it "rejects junk" $ parse "x" `shouldSatisfy` isLeft
  it "throws" $ launchMissiles `shouldThrow` anyException
  context "edge" $ it "empty" $ parse "" `shouldBe` Left Empty
```
Put `{-# OPTIONS_GHC -F -pgmF hspec-discover #-}` in `test/Spec.hs`; spec file names must end in `Spec.hs`, the module name must match the file name, and each exports `spec :: Spec`. Pass `--match PATTERN` to the test driver to run only matching spec items (the pattern is matched against the `/`-separated path or the pretty-printed path).

## Choosing
Tasty combines unit tests, golden tests and QuickCheck/SmallCheck properties (also Hedgehog via tasty-hedgehog) in one tree. Hspec offers describe/it specs, `shouldBe`/`shouldSatisfy`/`shouldThrow` expectations, spec hooks (`before`, `around`) and add-ons such as hspec-wai. The Tasty package page shows a cabal test-suite with `type: exitcode-stdio-1.0`.

## Gotchas
- Tests share resources: use `withResource` (Tasty) or `around`/`before` (Hspec) for DBs and servers.
- Golden files must be reviewed in the diff, never auto-accepted on CI.

## Self-check
- [ ] A failing test makes `cabal test` return non-zero.
- [ ] Test names are unique and filterable by pattern.

## Checked
2026-11-03. Confirmed against the Tasty, tasty-golden and Test.Tasty Hackage pages (testGroup, testCase, `@?=`, withResource, `-p` awk patterns, `-j`, `--accept`, goldenVsString) and the Hspec site pages (writing specs, expectations shouldBe/shouldSatisfy/shouldThrow, hspec-discover pragma and naming rules, `--match`, hooks before/around). Removed: `build-tool-depends`, `--test-show-details`, `cabal test --test-options` forms, `anyArithException`, hspec-golden and the seed-printing claim.
Method: documentation only; no commands were run.
