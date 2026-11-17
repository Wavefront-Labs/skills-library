---
id: computing-software.software-engineering.rust.test-fixtures-temp-dirs-and-test-data
name: test-fixtures-temp-dirs-and-test-data
category: computing-software
field: software-engineering
product: rust
tags: [rust, rust-testing, rust-test-fixtures, tempfile, fixtures, rstest, test-data]
level: practitioner
status: docs-checked
description: "Build isolated Rust test fixtures: tempfile temp dirs, rstest parameterised cases and fixtures, and locating test data via CARGO_MANIFEST_DIR."
sources:
  - https://docs.rs/tempfile
  - https://docs.rs/rstest/latest/rstest/
  - https://doc.rust-lang.org/cargo/reference/environment-variables.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Fixtures, temp dirs and test data

**Goal:** tests that do not touch the real filesystem or each other.

```rust
use tempfile::{tempdir, NamedTempFile};

#[test]
fn writes_report() {
    let dir = tempdir().unwrap();                      // recursively deleted on drop
    let out = dir.path().join("report.csv");
    generate(&out).unwrap();
    assert!(std::fs::read_to_string(&out).unwrap().starts_with("id,name"));
}

fn data(name: &str) -> std::path::PathBuf {
    std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("tests/data").join(name)
}

use rstest::{fixture, rstest};
#[fixture] fn db() -> TestDb { TestDb::new() }          // built fresh for each test using it
#[rstest]
#[case("a", 1)] #[case("bb", 2)]
fn lengths(#[case] s: &str, #[case] n: usize, db: TestDb) { assert_eq!(s.len(), n); let _ = db; }
```

- tempfile: `tempfile()` gives an unnamed file removed by the OS when the last handle closes; `NamedTempFile::new()` gives a file you can refer to by path; `tempdir()` gives a directory deleted recursively on drop; `spooled_tempfile()` is an in-memory buffer backed by a file when it grows.
- `CARGO_MANIFEST_DIR` is the directory containing your package's manifest; read it with `env!` at compile time to locate test data instead of depending on the working directory.
- rstest: `#[rstest]` with `#[case(...)]` for parameterised tests and `#[fixture]` functions injected by argument name.
- Build paths with `join` rather than hard-coded separators.

## Gotchas
- `TempDir` and `NamedTempFile` rely on destructors; cleanup does not happen if the process dies from an unhandled signal such as SIGINT or if the value is a static.
- Early drop: moving a `TempDir` into an API generic over `AsRef<Path>` consumes it and deletes the directory; pass a reference (`&dir`) instead. Hold the guard in a named variable, not `_`.
- `TempDir` and `NamedTempFile` use paths, so on Unix a temporary-file cleaner can invalidate them for very long-lived files; temporary directories are created with default permissions (world-readable unless umask or temp dir changes).
- Tests run in parallel threads by default: avoid shared fixed paths and ports.

## Verify
Run `cargo test` several times; no flakes and no leftover files in the repo (`git status` clean).

## Checked
Method: docs-checked 2026-11-09 against the docs.rs tempfile crate page (read in full), the rstest crate page (examples for rstest, case and fixture) and the cargo environment-variables reference (CARGO_MANIFEST_DIR). Dropped unconfirmed claims about cwd of tests, serial_test, nextest, tracing-test, OnceLock, set_var and testcontainers.
