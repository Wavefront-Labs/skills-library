---
id: computing-software.software-engineering.rust.snapshot-testing-with-insta
name: snapshot-testing-with-insta
category: computing-software
field: software-engineering
product: rust
tags: [rust, rust-testing, rust-insta, insta, snapshot-testing, cargo-insta]
level: practitioner
status: docs-checked
description: "Test complex Rust outputs with insta snapshots: assert_snapshot, assert_yaml_snapshot, redactions, inline snapshots and the cargo insta review workflow."
sources:
  - https://insta.rs/docs/quickstart/
  - https://insta.rs/docs/redactions/
  - https://insta.rs/docs/settings/
  - https://insta.rs/docs/advanced/
  - https://insta.rs/docs/cli/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Snapshot testing with insta

**Goal:** assert on large structured output without hand-writing expected values.

```toml
[dev-dependencies]
insta = { version = "1", features = ["yaml", "redactions", "json"] }
```
```rust
#[test]
fn renders_invoice() {
    let inv = build_invoice();
    insta::assert_yaml_snapshot!(inv, {
        ".id" => "[uuid]",                       // redact unstable fields
    });
    insta::assert_snapshot!(render_html(&inv));  // plain text snapshot
    insta::assert_snapshot!(inv.total(), @"12.50"); // inline snapshot, stored in the source
}
```

- Macros: `assert_snapshot!` for a string you produce, `assert_yaml_snapshot!`, `assert_json_snapshot!`, `assert_toml_snapshot!`, `assert_ron_snapshot!`, `assert_csv_snapshot!` for `serde::Serialize` values, and `assert_debug_snapshot!` for `Debug` output. YAML is recommended for real applications: it diffs well and supports redactions (cargo feature `redactions`).
- Workflow: run the tests; new snapshots are written beside the old ones with a `.snap.new` extension (when no CI is detected). `cargo insta review` reviews them interactively; `cargo insta test` collects all changes from a run with several assertions per test, and `cargo insta test --review` combines the two. Committed snapshots use `.snap`.
- `INSTA_UPDATE` controls writing: `auto` (default; `no` in CI, `new` otherwise), `always`, `unseen`, `new`, `no`. Insta detects CI from the `CI` environment variable, so make sure your CI system sets it; in CI no new snapshot files are written.
- Inline snapshots take `@"..."` as the last argument and are updated in the source file on review.
- `insta::with_settings!({ sort_maps => true }, { ... })` sorts maps for deterministic output; `glob!("inputs/*.txt", |path| { ... })` runs a snapshot per matching input file. `with_settings!` also takes `description`, `info` and `omit_expression` to make review easier.
- Remove snapshots no longer referenced with `cargo insta test --unreferenced=delete`.

## Gotchas
- Snapshots of non-deterministic data (timestamps, map order, absolute paths, UUIDs) create flaky tests; redact or sort.
- Snapshot files are committed, so do not snapshot secrets.
- Keep each snapshot focused so the diff is reviewable.
- Insta runs better when compiled with optimisation: set `insta.opt-level = 3` and `similar.opt-level = 3` under `[profile.dev.package]`.

## Verify
Change the output slightly: the test fails with a diff; `cargo insta review` accepts it; re-running passes and `git status` shows only the `.snap` change.

## Checked
Method: docs-checked 2026-11-09 against the insta quickstart, redactions, settings, advanced and cargo-insta CLI pages. Dropped the unconfirmed snapshots directory location and the claim that `INSTA_UPDATE=no` is needed explicitly in CI.
