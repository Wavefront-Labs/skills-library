---
id: computing-software.software-engineering.rust.cross-compiling-rust
name: cross-compiling-rust
category: computing-software
field: software-engineering
product: rust
tags: [rust, rust-cross-compilation, cargo-zigbuild, cross-rs, musl, target-triples, linkers, aarch64, static-linking]
level: advanced
status: docs-checked
description: "Cross-compile Rust binaries: target triples, linker configuration in .cargo/config.toml, cross (Docker), cargo-zigbuild for glibc versions, musl static builds and C dependencies."
sources: ["https://doc.rust-lang.org/rustc/platform-support.html", "https://doc.rust-lang.org/cargo/reference/config.html#targettriplelinker", "https://github.com/cross-rs/cross", "https://github.com/rust-cross/cargo-zigbuild"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cross-compiling Rust

**Goal:** build binaries for other OS/CPU combinations (ARM servers, Raspberry Pi, static Linux,
Windows) from one machine or CI runner.

## Pieces you need
1. **Target std**: `rustup target add aarch64-unknown-linux-gnu`.
2. **A linker** (and C toolchain/sysroot if any crate builds C code via `cc`).
3. Cargo told which linker to use.
`cargo build --target aarch64-unknown-linux-gnu --release` writes to `target/<triple>/release/`.

Common triples: `x86_64-unknown-linux-gnu`, `x86_64-unknown-linux-musl` (static),
`aarch64-unknown-linux-gnu`, `armv7-unknown-linux-gnueabihf`, `x86_64-pc-windows-gnu` /
`-msvc`, `aarch64-apple-darwin`, `wasm32-unknown-unknown`, `wasm32-wasip2`.

## Option 1: system cross toolchain
```bash
# install a cross GCC that provides aarch64-linux-gnu-gcc
```
`.cargo/config.toml`:
```toml
[target.aarch64-unknown-linux-gnu]
linker = "aarch64-linux-gnu-gcc"
```
For `cc`-built C code also set `CC_aarch64_unknown_linux_gnu=aarch64-linux-gnu-gcc`; for openssl-sys
you need target OpenSSL headers and libraries.

## Option 2: cross (Docker images with toolchains)
```bash
cargo install cross --git https://github.com/cross-rs/cross
cross build --target aarch64-unknown-linux-gnu --release
cross test  --target armv7-unknown-linux-gnueabihf
```
Customise images via `Cross.toml` (`pre-build` apt installs for system libraries). Needs Docker or
Podman.

## Option 3: cargo-zigbuild (Zig as linker)
```bash
cargo install --locked cargo-zigbuild   # or: pip install cargo-zigbuild (also installs ziglang)
cargo zigbuild --release --target aarch64-unknown-linux-gnu.2.17   # target glibc 2.17
cargo zigbuild --release --target universal2-apple-darwin           # macOS fat binary
```
The `.2.17` suffix links against an older glibc symbol set so the binary runs on old distros - the
main reason to choose zigbuild for Linux release artifacts. No Docker needed.

## Static Linux binaries with musl
```bash
rustup target add x86_64-unknown-linux-musl
cargo build --release --target x86_64-unknown-linux-musl
file target/x86_64-unknown-linux-musl/release/app   # "statically linked"
```
Good for `FROM scratch` images.

## macOS and Windows
- Apple targets need the macOS SDK; the cargo-zigbuild project publishes Docker images with the SDK pre-installed (check the SDK licence terms), or use macOS CI runners.
- Windows from Linux: `x86_64-pc-windows-gnu` with a mingw-w64 toolchain.

## CI release matrix
Matrix over targets with `cross` or zigbuild on Linux runners and native macOS/Windows runners.

## Verify
- [ ] `file` shows the expected architecture.
- [ ] Binary runs on the target (device, `cross test`, or a CI job on that arch).

## Checked

2026-10-25. Checked against the rustc platform-support page, the Cargo Book config reference (`[target.<triple>] linker`), the cc crate docs (`CC_<target_with_underscores>`), the cross README (install from git, Docker or Podman, `pre-build` in Cross.toml) and the cargo-zigbuild README (`cargo install --locked`, `pip install cargo-zigbuild`, glibc suffix such as `.2.17`, `universal2-apple-darwin`, Docker images with macOS SDK). All listed triples appear in platform-support, including `wasm32-wasip2` (Tier 2 since Rust 1.82). Removed unconfirmed claims: QEMU use by `cross test`, musl allocator and DNS behaviour, `cargo-xwin`, `cargo-dist`, the Debian package name, mingw linker name and objdump checks.

Method: documentation only; no commands were run.
