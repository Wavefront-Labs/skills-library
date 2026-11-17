---
id: computing-software.software-engineering.zig.zig-cc-compiler
name: zig-cc-compiler
category: computing-software
field: software-engineering
product: zig
tags: [zig, zig-cc-compiler, zig-cli-tooling, zig-cc, zig-c++, cgo-zig, cross-c, clang-drop-in]
level: advanced
status: docs-checked
description: "Use zig cc and zig c++ as a cross-compiling clang replacement for C projects, Go cgo, Rust cc-rs and Makefiles, including glibc version targeting."
sources:
  - https://github.com/ziglang/zig/blob/0.15.1/src/main.zig
  - https://ziglang.org/documentation/0.15.1/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# zig cc and zig c++ as drop-in C/C++ compilers
**Goal:** cross-compile C without installing toolchains.

```bash
zig cc -target x86_64-linux-musl -O2 -o hello hello.c
zig c++ -target aarch64-linux-gnu.2.28 -o app app.cpp
CC="zig cc -target x86_64-linux-musl" make
```
- `zig cc` and `zig c++` are listed by `zig --help` as "drop-in C compiler" and "drop-in C++ compiler"; `zig ar`, `zig ranlib`, `zig dlltool`, `zig lib`, `zig objcopy` and `zig rc` are the matching drop-in tools.
- `-target <arch><sub>-<os>-<abi>` selects the target; a glibc version can be appended to the ABI (`-target x86_64-linux-gnu.2.17`), which the `Target.Query` parser reads as `glibc_version`.
- Build tools that cannot pass a multi-word `CC` need a wrapper script that runs `exec zig cc -target <triple> "$@"`.
- Zig's C-source support needs its Clang backend ("requires LLVM extensions" in the file-type table). Flags after `-cflags ... --` apply to the following C files when using `zig build-exe`.
- C undefined-behavior detection has its own flags: `-fsanitize-c[=trap|full]` and `-fno-sanitize-c`.

## Self-check
Build a C hello world for `x86_64-windows-gnu` from your host and check that `file` reports PE32+.

## Checked
2026-11-02. Confirmed in 0.15.1 `src/main.zig` usage text (drop-in tools, `-target`, `-fsanitize-c`, `-cflags`, LLVM-extension note) and `lib/std/Target/Query.zig` (glibc version in the ABI part).
Removed: Go cgo, Rust cc crate and CMake recipes, "UBSan on by default in Debug", "-march=native becomes -mcpu=native", "macOS targets lack SDK frameworks", the autoconf `--host=` hint, the compiled-libc cache claim.
Method: documentation only; no commands were run.
