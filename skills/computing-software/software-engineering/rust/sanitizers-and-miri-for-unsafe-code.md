---
id: computing-software.software-engineering.rust.sanitizers-and-miri-for-unsafe-code
name: sanitizers-and-miri-for-unsafe-code
category: computing-software
field: software-engineering
product: rust
tags: [rust, rust-security, rust-sanitizers, sanitizers, asan, tsan, msan, miri, undefined-behavior]
level: advanced
status: docs-checked
description: "Run AddressSanitizer, ThreadSanitizer and Miri against Rust code with unsafe or FFI, using nightly flags, and interpret the reports."
sources:
  - https://doc.rust-lang.org/unstable-book/compiler-flags/sanitizer.html
  - https://github.com/rust-lang/miri
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Sanitizers and Miri

**Goal:** catch memory errors and data races in unsafe/FFI code that the borrow checker cannot see.

Sanitizers are unstable `-Z` flags (nightly) and the docs strongly recommend combining them with a rebuilt, instrumented standard library via `-Zbuild-std`:

```bash
rustup toolchain install nightly --component rust-src
# AddressSanitizer: out-of-bounds, use-after-free, double free, leaks
RUSTFLAGS="-Zsanitizer=address" cargo +nightly test -Zbuild-std --target x86_64-unknown-linux-gnu
# ThreadSanitizer: data races
RUSTFLAGS="-Zsanitizer=thread" cargo +nightly test -Zbuild-std --target x86_64-unknown-linux-gnu
# MemorySanitizer: uninitialised reads; -Zbuild-std is strictly necessary
RUSTFLAGS="-Zsanitizer=memory -Zsanitizer-memory-track-origins" cargo +nightly test -Zbuild-std --target x86_64-unknown-linux-gnu
```

Leak detection is on by default on Linux and needs `ASAN_OPTIONS=detect_leaks=1` on macOS; use-after-return needs `ASAN_OPTIONS=detect_stack_use_after_return=1`. Symbolised stack traces need `llvm-symbolizer` in `PATH`.

Miri (`rustup +nightly component add miri`, then `cargo miri test`) interprets the program and detects out-of-bounds access, use-after-free, uninitialised data, misaligned access, invalid values, data races, leaks, and (experimental) Stacked Borrows or Tree Borrows aliasing violations. Flags go in `MIRIFLAGS`; `-Zmiri-strict-provenance` makes integer-to-pointer casts stop execution.

Split roles: Miri for unsafe abstractions in your crate; sanitizers for FFI-heavy code Miri cannot run.

## Gotchas
- ASan targets include `x86_64-unknown-linux-gnu`, `aarch64-unknown-linux-gnu`, `x86_64-apple-darwin`, `aarch64-apple-darwin`; MSan is Linux/FreeBSD only; check the page's target lists for your target.
- Mixed C/Rust: if other languages are also instrumented you may need the `external-clangrt` flag.
- Miri runs as a platform-independent interpreter with no access to most platform APIs or FFI; it does not support networking.
- Miri isolation fakes env vars, clocks and entropy; `-Zmiri-disable-isolation` accesses the real system.
- Miri tests one of many possible executions. When it finds UB the code is unsound; a clean run is not proof.

## Verify
Plant a deliberate out-of-bounds `get_unchecked` read in a test and confirm Miri and ASan each report it; remove it.

## Checked
2026-11-09. Confirmed against the Rust Unstable Book sanitizer page (flags, `-Zbuild-std`, ASAN_OPTIONS, targets, MSan track-origins, llvm-symbolizer, external-clangrt) and the Miri README (detections, MIRIFLAGS, strict provenance, isolation, FFI and networking limits). Removed: "10 to 100 times slower", CARGO_TARGET_DIR, `ASAN_OPTIONS=detect_leaks=1:symbolize=1` as a general setting, Windows MSVC ASan claim, "all deps instrumented" for MSan, `cargo fuzz` pointer. The page's ASan target list was read; the TSan and MSan lists were read in part.
Method: documentation only; no commands were run.
