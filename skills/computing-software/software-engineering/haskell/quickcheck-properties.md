---
id: computing-software.software-engineering.haskell.quickcheck-properties
name: quickcheck-properties
category: computing-software
field: software-engineering
product: haskell
tags: [haskell, quickcheck, property-testing, arbitrary, shrink, forall, generators, coverage, hedgehog, quickcheck-properties]
level: practitioner
status: docs-checked
description: "Write properties with QuickCheck: Arbitrary instances, generators (choose, oneof, frequency, listOf), shrinking, implication, cover and classify, and monadic properties."
sources: ["https://hackage.haskell.org/package/QuickCheck/docs/Test-QuickCheck.html", "https://hackage.haskell.org/package/QuickCheck/docs/Test-QuickCheck-Monadic.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# QuickCheck

**Goal:** test laws over randomly generated inputs. Package: `QuickCheck`.

```haskell
import Test.QuickCheck
import Data.List (sort)

prop_reverse :: [Int] -> Bool
prop_reverse xs = reverse (reverse xs) == xs

prop_sorted :: [Int] -> Property
prop_sorted xs = let s = sort xs in
  length s === length xs .&&. and (zipWith (<=) s (drop 1 s))

prop_div :: Int -> NonZero Int -> Property
prop_div a (NonZero b) = b /= 0 ==> (a `div` b) * b + a `mod` b === a     -- ==> discards cases

data Color = R | G | B deriving (Show, Eq)
instance Arbitrary Color where arbitrary = elements [R, G, B]

genUser :: Gen User
genUser = User <$> choose (1, 99) <*> listOf (elements ['a'..'z'])

main = do
  quickCheck prop_reverse
  quickCheckWith stdArgs { maxSuccess = 1000 } prop_sorted
  verboseCheck prop_reverse
```

## Techniques
- Properties: round trips (`decode . encode == id`), invariants, model-based (compare to a simple model), idempotence, commutativity.
- Generators: `choose`, `elements`, `oneof`, `frequency`, `vectorOf`, `listOf`, `sized`, `scale`, `suchThat`; `genericShrink` derives a shrinker.
- `cover 20 cond "label"` and `classify`/`collect` check the distribution of inputs.
- `counterexample`, `===` (shows both sides), `forAll gen prop`, `forAllShrink`.
- Stateful and parallel testing: `Test.QuickCheck.Monadic` (`monadicIO`, `run`, `assert`).
- Failures are shrunk to a smaller counterexample; `Args` has `maxSuccess` and a `replay` field to rerun a test case.

## Gotchas
- `==>` discards test cases that fail the precondition; with a rare precondition most cases are discarded, so generate valid values directly (for example with `NonZero`).
- `Arbitrary` for recursive types needs size control (`sized`, `scale`).
- For properties that perform IO use `ioProperty`, or `monadicIO` from `Test.QuickCheck.Monadic`.

## Self-check
- [ ] Each property fails when a deliberately wrong implementation is used.
- [ ] Distribution checked with `cover` for non-uniform generators.

## Checked
2026-11-03. Confirmed against the Haddock pages for `Test.QuickCheck` and `Test.QuickCheck.Monadic`: `quickCheckWith`, `stdArgs`, `maxSuccess`, `replay`, `verboseCheck`, `===`, `.&&.`, `==>`, `NonZero`, `choose`, `elements`, `oneof`, `frequency`, `vectorOf`, `listOf`, `sized`, `scale`, `suchThat`, `genericShrink`, `cover`, `classify`, `collect`, `counterexample`, `forAll`, `forAllShrink`, `ioProperty`, `monadicIO`. Removed: Hedgehog mention, the "gave up" message, the claim that a seed is printed, and the remark that `suchThat` can be slow.
Method: documentation only; no commands were run.
