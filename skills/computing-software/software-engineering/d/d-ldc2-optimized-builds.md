---
id: computing-software.software-engineering.d.d-ldc2-optimized-builds
name: d-ldc2-optimized-builds
category: computing-software
field: software-engineering
product: d
tags: [d-ldc2-optimized-builds, ldc-gdc-compilers, ldc, ldc2, llvm, lto, pgo, cross-compilation, mtriple, mcpu, sanitizers, optimization, d]
level: practitioner
status: draft
description: "Build fast binaries with ldc2: -O3, -release, -flto=thin, -fprofile-instr-generate PGO, -mcpu=native, --mtriple cross targets, sanitizers and static linking options."
sources:
  - https://dlang.org/spec/spec.html
  - https://dlang.org/phobos/index.html
  - https://dub.pm/
  - https://ddili.org/ders/d.en/index.html
  - https://dlang.org/articles.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# ldc2: optimisation levels, LTO, PGO and cross compilation

Goal: get the best machine code from LDC.

- Basics: `ldc2 -O3 -release -boundscheck=off -mcpu=native app.d` (`-O` = `-O2`, `-O3`, `-Os`, `-Oz`); `-flto=thin` or `full` with `-defaultlib=phobos2-ldc-lto,druntime-ldc-lto` for LTO of the std lib; `-fvisibility=hidden`, `-link-defaultlib-shared=false` for static runtime.
- PGO: instrument `-fprofile-instr-generate=prof.raw`, run, `ldc-profdata merge`, then `-fprofile-instr-use=prof.profdata`.
- Cross: `ldc2 -mtriple=aarch64-linux-gnu -mcpu=cortex-a72 app.d` plus a matching cross-compiled druntime/phobos (use `ldc-build-runtime --ninja --targetSystem=...`); wasm: `-mtriple=wasm32-unknown-unknown-wasm -betterC`.
- Sanitizers: `-fsanitize=address|thread|undefined|fuzzer`; coverage `-cov`, `-fprofile-instr-generate`.
- Compat: ldc2 accepts most dmd flags; use `ldmd2` as a dmd-compatible driver (dub uses it with `--compiler=ldc2`, which maps flags).
- Attributes: `import ldc.attributes; @(ldc.attributes.llvmAttr("...")) `, `@fastmath`, `@optStrategy("minsize")`, `@target("avx2")`.
- Pitfalls: LDC lags behind dmd frontends by a release or two; check `ldc2 --version` for the frontend level.

Gotchas:
- `-mcpu=native` binaries do not run on older CPUs.
- `-ffast-math`-like (`@fastmath`) alters NaN/inf behaviour.

Verify: compare `objdump -d` size/speed on a hot loop between dmd -O and ldc2 -O3.
