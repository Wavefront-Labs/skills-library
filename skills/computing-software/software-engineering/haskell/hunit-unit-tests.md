---
id: computing-software.software-engineering.haskell.hunit-unit-tests
name: hunit-unit-tests
category: computing-software
field: software-engineering
product: haskell
tags: [haskell, hunit, assertequal, test-list, assertion, testcase, unit-test, hunit-unit-tests, haskell-testing]
level: intro
status: draft
description: "Write unit tests with HUnit: TestCase, assertEqual, (@?=), (@=?), assertBool, labels, running with runTestTT or via Tasty, and testing for exceptions."
sources: ["https://hackage.haskell.org/package//tasty", "https://hackage.haskell.org/package//HUnit", "https://hackage.haskell.org/package//QuickCheck"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# HUnit

**Goal:** plain example-based unit tests. Package: `HUnit`.

```haskell
import Test.HUnit

tests :: Test
tests = TestList
  [ "add"      ~: 3 @=? (1 + 2)                       -- expected @=? actual
  , "double"   ~: double 4 ~?= 8                       -- actual ~?= expected
  , "nonempty" ~: assertBool "must be non-empty" (not (null (items cfg)))
  , TestLabel "lookup" $ TestCase $ do
      r <- lookupUser "bob"
      assertEqual "name" (Just "bob") (fmap name r)
  ]

main :: IO ()
main = do
  Counts{failures, errors} <- runTestTT tests
  when (failures + errors > 0) exitFailure
```

## With Tasty (preferred runner)
```haskell
import Test.Tasty
import Test.Tasty.HUnit
main = defaultMain $ testGroup "unit"
  [ testCase "add" $ (1 + 2) @?= (3 :: Int)
  , testCase "throws" $ do
      r <- try (evaluate (1 `div` 0 :: Int))
      r @?= Left DivideByZero ]
```
`@?=` is actual-then-expected; `@=?` is expected-then-actual (mixing them yields swapped failure messages).

## Rules
- `assertFailure "msg"`, `assertEqual`, `assertBool`; a failed assertion throws `HUnitFailure`.
- Floating-point: compare with a tolerance (`abs (a - b) < 1e-9`).
- Show instances are needed on compared types; derive `Show, Eq`.
- Test pure functions via pure assertions; keep IO tests isolated (temp dirs).

## Gotchas
- `runTestTT` returns counts but does not set the exit code: check them.
- Lazy exceptions in `@?=` arguments are reported as test errors; fine, but use `evaluate` to catch them precisely.

## Self-check
- [ ] The test executable exits non-zero on failure (`cabal test` fails).
- [ ] Each test name describes behaviour.
