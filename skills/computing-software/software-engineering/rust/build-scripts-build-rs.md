---
id: computing-software.software-engineering.rust.build-scripts-build-rs
name: build-scripts-build-rs
category: computing-software
field: software-engineering
product: rust
tags: [rust, cargo, build-rs, build-script, cc-crate, code-generation, rerun-if-changed]
level: practitioner
status: docs-checked
description: "Write Cargo build scripts (build.rs): compiling C with cc, linking system libraries, generating code into OUT_DIR, rerun-if-changed hygiene and cross-compilation awareness."
sources:
  - https://doc.rust-lang.org/cargo/reference/build-scripts.html
  - https://doc.rust-lang.org/cargo/reference/build-script-examples.html
  - https://docs.rs/cc/latest/cc/
  - https://doc.rust-lang.org/cargo/reference/environment-variables.html#environment-variables-cargo-sets-for-build-scripts
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Build scripts (build.rs)

**Goal:** compile native code, link libraries or generate Rust code at build time, without making every build slow or non-reproducible.

## 1. Basics
`build.rs` at the package root is compiled and run before the crate. It communicates through `cargo::` lines on stdout (Rust 1.77+; older: `cargo:`).
```rust
// build.rs
fn main() {
    println!("cargo::rerun-if-changed=src/native/fast.c");
    println!("cargo::rerun-if-changed=build.rs");
    cc::Build::new()
        .file("src/native/fast.c")
        .flag_if_supported("-O3")
        .compile("fast");                       // emits link directives for libfast.a
}
```
```toml
[build-dependencies]
cc = "1"
```

## 2. Rerun hygiene
Without any `rerun-if-*` line, Cargo reruns the script whenever **any file in the package** changes. Always declare:
- `cargo::rerun-if-changed=PATH` (file or directory, checked by mtime)
- `cargo::rerun-if-env-changed=OPENSSL_DIR`

## 3. Linking system libraries
```rust
fn main() {
    if let Ok(lib) = pkg_config::Config::new().atleast_version("1.2").probe("zlib") {
        return;                                  // pkg-config emitted link + include info
    }
    println!("cargo::rustc-link-lib=z");
    println!("cargo::rustc-link-search=native=/opt/zlib/lib");
}
```
Convention: a `foo-sys` crate does the linking (with `links = "foo"` in its manifest) and exposes raw FFI; a safe `foo` crate wraps it. `links` lets dependents read metadata via `DEP_FOO_*` env vars.

## 4. Generating code
```rust
let out = std::path::PathBuf::from(std::env::var("OUT_DIR").unwrap());
std::fs::write(out.join("codes.rs"), generate_from("data/codes.csv"))?;
```
```rust
// src/lib.rs
include!(concat!(env!("OUT_DIR"), "/codes.rs"));
```
Never write into `src/` from build.rs (breaks `cargo package` verification and read-only sources). Protobuf: `prost-build`/`tonic-build` follow this pattern.

## 5. Custom cfgs
```rust
println!("cargo::rustc-check-cfg=cfg(has_avx512)");
if detect() { println!("cargo::rustc-cfg=has_avx512"); }
```

## 6. Cross-compilation awareness
build.rs runs on the **host**. Inspect the target with env vars Cargo provides: `TARGET`, `CARGO_CFG_TARGET_OS`, `CARGO_CFG_TARGET_ARCH`, `CARGO_CFG_TARGET_FEATURE`, not `cfg!(target_os)` (that is the host).

## Gotchas
- Build scripts can run arbitrary code at build time: review them in dependencies (supply chain).
- Network access in build.rs breaks offline/vendored builds and docs.rs; vendor sources instead.
- Warnings: `cargo::warning=message` shows to the user; panics fail the build with output shown.
- Slow scripts (big C builds) run once per profile/target; set `opt-level` under `[profile.dev.build-override]` only if the script itself is slow.

## Verify
- A second `cargo build` with no changes does not rerun the script, and `cargo package` + cross builds (`cargo build --target aarch64-unknown-linux-gnu`) succeed.

## Checked

2026-10-25. Checked against the Cargo Book build-scripts reference (Cargo repository doc/book, current main, Cargo 1.100 line) and the cc 1.x and pkg-config crate sources. Confirmed: `cargo::KEY=VALUE` syntax needs Rust 1.77; `rerun-if-changed` compares mtime and scans a directory; with no `rerun-if` lines Cargo scans the whole package directory; `cargo::rustc-check-cfg=cfg(...)`, `cargo::warning=`, `links` and `DEP_<LINKS>_<KEY>` metadata; `TARGET` and `CARGO_CFG_TARGET_*` incl. `CARGO_CFG_TARGET_FEATURE`; `cc::Build::flag_if_supported`/`compile`, `pkg_config::Config::atleast_version`/`probe`; `[profile.*.build-override]`. Removed an unconfirmed `cargo build -vv` verification detail.

Method: documentation only; no commands were run.
