---
id: computing-software.software-engineering.nim.zig-cc-musl-static-builds
name: zig-cc-musl-static-builds
category: computing-software
field: software-engineering
product: nim
tags: [zig-cc-musl-static-builds, cross-compilation, zig-cc, zigcc, musl, static, cross-compile, portable-binary, glibc, nim]
level: advanced
status: docs-checked
description: "Build static musl binaries from Nim by pointing the C compiler at zig cc (Nim --cc:env plus Zig -target), with what each doc does and does not cover."
sources:
  - https://nim-lang.org/docs/nimc.html
  - https://ziglang.org/learn/overview/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cross builds and static binaries with zig cc

Goal: produce a portable static Linux binary without installing a separate cross toolchain.

- Zig ships a C compiler front end, `zig cc`. Its overview page shows `zig build-exe hello.c -lc -target x86_64-linux-musl`: Zig builds musl libc from source and caches it, and `ldd` on the result prints "not a dynamic executable". The same page states glibc does not support static builds but musl does.
- Zig target triples are given with `-target` (the overview page shows `aarch64-linux-gnu`, `aarch64-linux` and `x86_64-windows`/`x86_64-macos` for `zig build-exe`); read Zig's target list before relying on one.
- Nim side: `nim c --cc:env file.nim` takes the C compiler from the `CC` environment variable (`nim cpp --cc:env` uses `CXX`); available since Nim 1.4. `--os:` and `--cpu:` set the Nim cross-compilation target, and `--passC:` / `--passL:` pass options to the C compiler and linker.
- Wiring them: make `CC` a small wrapper script that runs `zig cc -target x86_64-linux-musl "$@"`. Neither page documents Nim and Zig used together, so treat this as a recipe to test, not a guarantee.

Gotchas:
- Keep Nim's `--os`/`--cpu` and Zig's `-target` consistent.
- musl is a different libc from glibc; test the binary on the target.

Verify: `ldd ./app` prints "not a dynamic executable".

## Checked

2026-11-03. Confirmed in the Zig overview page: `zig cc`, the musl static example and `ldd` output, glibc cannot link statically. Confirmed in the Nim compiler guide: `--cc:env` with `CC`/`CXX`, `--os`, `--cpu`, `--passC`, `--passL`. Removed: Nim `--clang.exe`/`--clang.linkerexe` flags, glibc-version target suffixes, `getpwnam`/DNS behaviour claims, `-fno-sanitize=undefined`, and the nimble `zigcc` package claim (none are in the pages read).
Method: documentation only; no commands were run.
