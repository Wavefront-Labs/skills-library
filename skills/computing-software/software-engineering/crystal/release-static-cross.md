---
id: computing-software.software-engineering.crystal.release-static-cross
name: release-static-cross
category: computing-software
field: software-engineering
product: crystal
tags: [release-static-cross, cli-build-run, release, static, cross-compile, target, link-command, object-file, musl-static, optimization, crystal]
level: advanced
status: docs-checked
description: "Build release, fully static (musl or Alpine) or cross-compiled Crystal binaries: --release, --static, --cross-compile --target, and the printed link command."
sources:
  - https://github.com/crystal-lang/crystal-book/blob/master/docs/man/crystal/README.md
  - https://github.com/crystal-lang/crystal-book/blob/master/docs/guides/static_linking.md
  - https://github.com/crystal-lang/crystal-book/blob/master/docs/syntax_and_semantics/cross-compilation.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# --release, --static and --cross-compile

Goal: ship an optimised static binary.

- Release: `crystal build hello_world.cr --release`.
- Static: `crystal build hello_world.cr --release --static`. Fully static executables are currently supported only on Alpine Linux (musl). All dependencies need static libraries at compile time; `CRYSTAL_LIBRARY_PATH` is the first lookup place for libraries and can supply static versions.
- `glibc` does not play well with static linking and it is highly discouraged; link against `musl-libc` instead (the result also runs on glibc systems). Official Alpine images are `crystallang/crystal:latest-alpine`; they ship static versions of the standard library's dependencies.
- Cross: `crystal build your_program.cr --cross-compile --target "x86_64-unknown-linux-gnu"` writes a `.o` file and prints a `cc ...` command to run on the target system, which finishes the executable. `--target` is an LLVM target triple that also sets the default compile-time flags; `llvm-config --host-target` on the target gives its triple. Use `-D` for flags not implied by the target.
- `crystal version` prints the Crystal version, LLVM version and default target triple.
- `--mcpu CPU` and `--mattr` set target CPU and features; `--prelude` selects a prelude file.

Gotchas:
- macOS does not officially support fully static linking, and Windows MSVC does not either; `openssl` and `glibc` are known for static-linking complications.
- Static libraries end in `.a` (POSIX) and `.lib` (MSVC); the cross-compile link command lists the libraries the target needs (the manual shows `-lpcre -lrt -lm -lgc -lunwind`).

Verify: `ldd` on a fully static binary prints "statically linked".

## Checked

2026-11-03. Confirmed against the Crystal compiler manual (release and static sections, `crystal version`), the Static Linking guide (glibc versus musl, Alpine images, `CRYSTAL_LIBRARY_PATH`, per-platform notes, `ldd` output) and the Cross-compilation page (`--cross-compile`, `--target`, `.o` and printed link command).
Fixed: the target triple example `aarch64-linux-musl` and the claim that the object is `app.o` were replaced by the documented form; the default target is shown by `crystal version`, not `crystal --version`. Removed: the DNS/musl resolver claim and the list libevent/openssl as required target libraries.
Method: documentation only; no commands were run.
