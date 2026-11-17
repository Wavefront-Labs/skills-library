---
id: computing-software.software-engineering.rust.debugging-rust-with-gdb-and-lldb
name: debugging-rust-with-gdb-and-lldb
category: computing-software
field: software-engineering
product: rust
tags: [rust, rust-debugging-diagnostics, rust-debuggers, gdb, lldb, rust-gdb, rust-lldb, debug-symbols, core-dumps]
level: practitioner
status: draft
description: "Debug Rust programs with rust-gdb or rust-lldb: debug profiles, pretty-printers, breakpoints, core dumps, and VS Code CodeLLDB."
sources:
  - https://doc.rust-lang.org/rustc/codegen-options/index.html
  - https://www.rust-lang.org/tools/install
  - https://github.com/vadimcn/codelldb
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Debugging Rust with gdb and lldb

**Goal:** step through code, inspect `Vec`/`String`/`HashMap`, and analyse crashes.

The rustup toolchain ships wrappers that load Rust pretty-printers: `rust-gdb` and `rust-lldb`.

```bash
cargo build                             # dev profile has debug = true
rust-gdb target/debug/app
(gdb) break app::parse                  # function path
(gdb) break src/main.rs:42
(gdb) run --flag arg
(gdb) bt                                # backtrace
(gdb) info locals
(gdb) p v                               # Vec pretty-printed
(gdb) set print pretty on
(gdb) watch counter                     # hardware watchpoint

rust-lldb target/debug/app -- --flag
(lldb) b main.rs:42
(lldb) frame variable
(lldb) expr -- v.len()                  # expression evaluation is limited for generics
```

Optimised builds: add symbols to release with `[profile.release] debug = 1` (line tables) or `debug = true`; `split-debuginfo = "packed"`; keep frame pointers for profilers (`RUSTFLAGS="-C force-frame-pointers=yes"`). Inlining and optimisation reorder code and hide variables ("optimized out"); debug with `opt-level = 0` or `1` when possible.

Core dumps: `ulimit -c unlimited` (Linux; check `core_pattern` or `coredumpctl`), then `rust-gdb target/debug/app core`. Panics: break on `rust_panic` (`break rust_panic`) or set `RUST_BACKTRACE=full`; `RUST_LOG`/tracing for run-time insight. VS Code: CodeLLDB extension with `cargo` launch configuration, or `rust-analyzer` "Debug" lens. On Windows use the MSVC toolchain with WinDbg/VS debugger (`.pdb` files).

## Gotchas
- Pretty-printers depend on the std source layout; mismatched debugger and toolchain versions show raw structs.
- Async code: state machines appear as generated structs; use `tokio-console` or `tracing` instead of stepping.
- `println!`-style debugging may change timing for races; use `rr` (record and replay) on Linux for nondeterministic bugs: `rr record ./app; rr replay`.

## Verify
Set a breakpoint in a function you call in a test, run until hit, print a `HashMap` local and confirm the entries show as key-value pairs.
