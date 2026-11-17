---
id: computing-software.software-engineering.d.d-mir-ion-random-and-linalg
name: d-mir-ion-random-and-linalg
category: computing-software
field: software-engineering
product: d
tags: [d-mir-ion-random-and-linalg, ecosystem-mir, mir-ion, mir-random, lubeck, mir-lapack, mir-blas, serialization, linear-algebra, rng, numeric-libraries, asdf, d]
level: advanced
status: draft
description: "Use mir-ion for fast JSON/Ion/CSV serialization, mir-random for RNG engines and distributions, lubeck/mir-lapack for linear algebra, and mir-cpuid, mir-optim."
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

# Mir ecosystem: mir-ion serialization, mir-random, lubeck linear algebra

Goal: pick the right Mir package.

- Serialization: `mir-ion` (`import mir.ser.json; auto s = serializeJson(myStruct);`, `import mir.deser.json; auto v = deserializeJson!MyStruct(text);`, plus Ion binary, Amazon Ion text, CBOR, CSV via `mir.csv`); attributes `@serdeKeys("a","b")`, `@serdeIgnore`, `@serdeOptional`, `@serdeProxy`, `@serdeFallbackStruct`; struct-based, allocation-light. `asdf` is the predecessor with similar API.
- Random: `mir-random` (`import mir.random; import mir.random.variable; auto rng = Random(unpredictableSeed); auto x = uniformVar(0.0, 1.0)(rng);`, `normalVar`, `gammaVar`, `shuffle`, `rand!T`), engines `Xoshiro256StarStar`, `Mt19937`; thread-local `threadLocal!Random`.
- Linear algebra: `lubeck` (`mtimes`, `mldivide`/`solve`, `svd`, `eigSymmetric`, `inv`, `det`, `pca`) over OpenBLAS/LAPACK: add `libs "openblas"` (or `dub` subconfiguration `"lubeck" "openblas"`); lower-level `mir-lapack`, `mir-blas`, `mir-optim` (least squares, root finding), `mir-stat`, `mir-interpolate`, `mir-cpuid`.
- Build: use LDC with `-O3 -mcpu=native -release`; avoid dmd for heavy numerics.

Gotchas:
- BLAS/LAPACK shared libs must be installed on the target system and linked at build.
- Package names and APIs shift across major versions (confirm on code.dlang.org).

Verify: mtimes on a 2x2 identity and check the result equals the input.
