---
id: computing-software.software-engineering.rust.unit-integration-and-doc-tests
name: unit-integration-and-doc-tests
category: computing-software
field: software-engineering
product: rust
tags: [rust, rust-testing, cargo-test, doc-tests, integration-tests, cargo-nextest, test-organization, rust-nextest]
level: practitioner
status: verified
description: "Organise Rust tests: unit tests in cfg(test) modules, integration tests in tests/, doc tests, test filtering and output, nextest, and testing private vs public APIs."
sources:
  - https://doc.rust-lang.org/book/ch11-00-testing.html
  - https://doc.rust-lang.org/cargo/commands/cargo-test.html
  - https://doc.rust-lang.org/rustdoc/write-documentation/documentation-tests.html
  - https://nexte.st/
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Unit, integration and doc tests in Rust

**Goal:** fast unit tests next to the code, black-box integration tests of the public API, and documentation examples that are guaranteed to compile.

## 1. Unit tests
```rust
pub fn split_amount(total: u64, parts: u64) -> Vec<u64> { ... }

#[cfg(test)]
mod tests {
    use super::*;                     // private items are accessible

    #[test]
    fn splits_evenly_with_remainder_first() {
        assert_eq!(split_amount(10, 3), vec![4, 3, 3]);
    }

    #[test]
    #[should_panic(expected = "parts must be > 0")]
    fn zero_parts_panics() { split_amount(1, 0); }

    #[test]
    fn parses() -> Result<(), Box<dyn std::error::Error>> {   // `?` in tests
        let v: Config = "a=1".parse()?;
        assert_eq!(v.a, 1);
        Ok(())
    }
}
```
`#[cfg(test)]` excludes the module from normal builds. Use `assert!`, `assert_eq!`, `assert_ne!` with custom messages; `pretty_assertions` for readable diffs.

## 2. Integration tests
Files in `tests/` are separate crates that only see the **public** API:
```
tests/
  api.rs
  common/mod.rs        # shared helpers (not tests/common.rs, which would be its own test crate)
```
Each `tests/*.rs` file compiles to its own binary (slow link times with many files); group into `tests/it/main.rs` with modules for big suites. Binary-only crates: move logic into `lib.rs` so it can be integration-tested.

## 3. Doc tests
```rust
/// Splits `total` into `parts` near-equal amounts.
///
/// ```
/// use acme_money::split_amount;
/// assert_eq!(split_amount(10, 3), vec![4, 3, 3]);
/// ```
///
/// ```should_panic
/// acme_money::split_amount(1, 0);
/// ```
```
Attributes: `no_run` (compile only), `ignore`, `compile_fail` (asserts it does not compile, great for API misuse), hidden setup lines with `# `. Doc tests only run for library crates.

## 4. Running
```bash
cargo test                          # unit + integration + doc tests
cargo test split                    # filter by name substring
cargo test --lib / --doc / --test api
cargo test -- --nocapture           # show println! output
cargo test -- --ignored             # run #[ignore] slow tests
cargo test -- --test-threads=1      # serialise tests sharing global state
cargo nextest run                   # process-per-test, faster, better output and retries (no doc tests)
```

## Gotchas
- Tests run in parallel threads by default; shared files, env vars (`std::env::set_var` is unsafe in edition 2024) and ports cause flakiness. Use temp dirs (`tempfile`), random ports, or nextest's process isolation.
- `#[should_panic]` without `expected` passes for any panic, including the wrong one.
- Async tests need a runtime attribute: `#[tokio::test]`.
- Test-only dependencies go under `[dev-dependencies]`.

## Verify
- `cargo test --workspace --all-features` runs all three kinds in CI, and breaking a doc example fails the build.
