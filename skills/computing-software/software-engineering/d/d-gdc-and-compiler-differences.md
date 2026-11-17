---
id: computing-software.software-engineering.d.d-gdc-and-compiler-differences
name: d-gdc-and-compiler-differences
category: computing-software
field: software-engineering
product: d
tags: [d-gdc-and-compiler-differences, ldc-gdc-compilers, gdc, gcc, version-gnu, compiler-choice, dmd-vs-ldc, frelease, fno-bounds-check, gdc-flags, architectures, d]
level: practitioner
status: draft
description: "Use GDC (GCC D frontend) for GCC-based toolchains and architectures, know flag differences (-fno-bounds-check, -O2, -frelease), version(GNU), and a compiler selection guide."
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

# GDC and choosing between dmd, ldc2 and gdc

Goal: choose a compiler for the job.

- GDC (`gdc` / `gdc-NN`, part of GCC since 9): flags look like GCC: `gdc -O2 -frelease -fno-bounds-check -funittest -fversion=Foo -finline-functions app.d -o app`; `-fdebug`, `-fdoc`, `-fno-druntime`/`-fno-moduleinfo` (betterC-like), `-fpreview=dip1000`, `-Wall`, `-g`.
- `version (GNU)` identifies it; extended asm per GCC syntax; `gcc.attributes` (`@attribute("noinline")`, `@target`).
- Strengths: any GCC target (many embedded and exotic architectures: SH, MIPS, RISC-V, S390x), distro packaging, GCC optimisations. Frontend often lags dmd.
- Guide: dmd for fast iteration and latest language features; ldc2 for release performance and cross targets (ARM, wasm, Android, Apple Silicon); gdc where GCC infra is required.
- dub: `dub build --compiler=gdc` (flags mapped; some dub settings unsupported).
- CI matrix: build with dmd (latest), ldc2 (latest and one older), optionally gdc; test `unittest` and release builds.
- Keep code portable: avoid dmd-only asm (`D_InlineAsm_X86_64`), `core.simd` differences, `real` precision assumptions (`real.sizeof` varies).

Gotchas:
- Different compilers disagree on `-preview` support; guard flags per compiler via dub `dflags-ldc`/`dflags-gdc`.
- The `real` type is 80 bit only on x86 dmd/ldc/gdc; elsewhere 64 or 128.

Verify: run the same unittest suite under all three compilers.
