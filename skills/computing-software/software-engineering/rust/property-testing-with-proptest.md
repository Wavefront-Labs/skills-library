---
id: computing-software.software-engineering.rust.property-testing-with-proptest
name: property-testing-with-proptest
category: computing-software
field: software-engineering
product: rust
tags: [rust, rust-testing, proptest, property-based-testing, quickcheck, shrinking, strategies]
level: practitioner
status: docs-checked
description: "Find edge cases in Rust code with proptest: strategies, prop_compose, shrinking, regression files, configuration and choosing good properties."
sources:
  - https://proptest-rs.github.io/proptest/intro.html
  - https://docs.rs/proptest/latest/proptest/
  - https://proptest-rs.github.io/proptest/proptest/failure-persistence.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Property testing with proptest

**Goal:** generate many inputs per test, shrink failures to minimal counterexamples, and keep regressions pinned.

## 1. A first property
```rust
use proptest::prelude::*;

proptest! {
    #[test]
    fn roundtrip_base64(data in proptest::collection::vec(any::<u8>(), 0..1024)) {
        let enc = encode(&data);
        prop_assert_eq!(decode(&enc).unwrap(), data);
    }

    #[test]
    fn split_preserves_total(total in 0u64..1_000_000, parts in 1u64..100) {
        let v = split_amount(total, parts);
        prop_assert_eq!(v.iter().sum::<u64>(), total);
        prop_assert_eq!(v.len() as u64, parts);
        prop_assert!(v.iter().max().unwrap() - v.iter().min().unwrap() <= 1);
    }
}
```
Use the `prop_assert*` macros, which fail the test case by returning an error rather than panicking.

## 2. Strategies
```rust
"[a-z]{1,16}"                                  // regex strategy for String
any::<u32>(), 1..=100i32, prop::bool::ANY
prop::collection::hash_map("[a-z]{3}", 0..10u8, 0..20)
prop_oneof![Just(Op::Clear), (0..10u32).prop_map(Op::Push)]
(0..100i64).prop_filter("non-zero", |x| *x != 0)    // use sparingly

prop_compose! {
    fn arb_range()(lo in 0i64..1000)(lo in Just(lo), hi in lo..2000) -> (i64, i64) { (lo, hi) }
}

#[derive(Debug, Clone, proptest_derive::Arbitrary)]
struct Order { qty: u16, price_cents: u32 }
```
Generate valid data by construction (dependent strategies, `prop_flat_map`) instead of filtering most cases away (proptest gives up after too many rejected values: see `max_local_rejects` and `max_global_rejects`).

## 3. Shrinking and regressions
On failure proptest shrinks to a minimal case and persists it in a file named after the source file, in a directory tree rooted at `proptest-regressions`. Later runs replay those cases before generating new ones. **Commit that directory** so collaborators and CI replay them too.

## 4. Configuration
```rust
proptest! {
    #![proptest_config(ProptestConfig { cases: 1000, max_shrink_iters: 10_000, ..ProptestConfig::default() })]
    #[test] fn heavy(x in any::<u64>()) { ... }
}
```
The default is 256 successful cases. Environment: `PROPTEST_CASES=10000 cargo test` for a nightly deep run.

## 5. Good properties
Round-trip (encode/decode, serialize/parse), oracle (compare with a simple reference implementation, e.g. a `Vec` model for a custom collection), invariants (sortedness, totals, no panics on arbitrary input), idempotence, commutativity. For state machines, `proptest-state-machine` generates operation sequences against a model.

## Gotchas
- `any::<f64>()` generates positive, negative, zero, subnormal and normal values but not infinities or NaN; use `proptest::num::f64::ANY` to include them, or a range (`-1e6..1e6f64`) to bound the domain, and compare with tolerances.
- Slow code under test multiplied by 256 default cases slows CI; reduce cases for heavy tests, raise them in nightly jobs.
- `quickcheck` is an alternative that generates and shrinks values by type alone, whereas proptest uses explicit `Strategy` objects; use `cargo fuzz` for coverage-guided fuzzing.

## Verify
- Introduce an off-by-one: the test fails with a small shrunk input and a new line in `proptest-regressions/`, which then reproduces deterministically.

## Checked

2026-10-25. Checked against the proptest repository: the book (failure persistence, configuring the number of cases with the default of 256 and `PROPTEST_CASES`, filtering and rejects, `prop_compose!`, comparison with QuickCheck) and the sources (`ProptestConfig` fields `max_shrink_iters`, `max_local_rejects`, `max_global_rejects`; `prop::bool::ANY`; `prop::collection::hash_map(key, value, size)`; the `Arbitrary` implementation for `f64`). Wrong in the draft and fixed: `any::<f64>()` does not generate NaN or infinity (the `Arbitrary` impl limits floats to positive, negative, zero, subnormal and normal values; `num::f64::ANY` includes infinities and quiet NaNs). Removed the unconfirmed `bolero` and shrinking-quality remarks.

Method: documentation only; no commands were run.
