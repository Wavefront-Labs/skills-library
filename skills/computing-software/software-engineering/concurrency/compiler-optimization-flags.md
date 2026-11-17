---
id: computing-software.software-engineering.concurrency.compiler-optimization-flags
name: compiler-optimization-flags
category: computing-software
field: software-engineering
product: concurrency
tags: [performance, compiler-optimization-flags, gcc, clang, lto, pgo, march]
level: advanced
status: draft
description: "Choose compiler optimisation flags for C, C++ and Rust: -O2 vs -O3, -march/-mtune, LTO, PGO, fast-math risks, frame pointers, and measuring that a flag actually helps."
sources: ["https://gcc.gnu.org/onlinedocs/gcc/Optimize-Options.html", "https://clang.llvm.org/docs/UsersManual.html#profile-guided-optimization", "https://doc.rust-lang.org/cargo/reference/profiles.html", "https://gcc.gnu.org/onlinedocs/gcc/x86-Options.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Compiler optimisation flags (-O2 / -O3 / -march / LTO)

## Optimisation levels (GCC/Clang)
| Flag | Use |
|---|---|
| `-O0` | debugging; no optimisation |
| `-Og` | debug builds that stay reasonably fast and debuggable |
| `-O2` | default for release in most distros and projects; safe, good speed/size |
| `-O3` | more aggressive inlining and vectorisation; sometimes faster, sometimes bigger/slower. Measure. |
| `-Os` / `-Oz` | size (embedded, cache-constrained, mobile) |
| `-Ofast` | `-O3` + `-ffast-math`: breaks IEEE semantics (NaN/inf checks, associativity); avoid unless numerics are validated |

## Target CPU
- `-march=x86-64-v3` (AVX2, BMI, FMA: Haswell+/Zen) or `-march=native` (this machine only; binaries
  may crash with illegal instruction elsewhere). `-mtune=` tunes scheduling without new instructions.
- For distributed binaries pick a baseline (`x86-64-v2`/`v3`) or use function multiversioning
  (`__attribute__((target_clones("avx2","default")))`).
- Rust: `RUSTFLAGS="-C target-cpu=x86-64-v3"`.

## Link-time optimisation (LTO)
`-flto` (GCC), `-flto=thin` (Clang ThinLTO: parallel, near-full benefit). Enables cross-file
inlining; typically 0-10% faster, smaller binaries, longer links. All objects and static libs must be
built with compatible LTO. Rust: `lto = "thin"` or `"fat"`, `codegen-units = 1` for max optimisation.

## Profile-guided optimisation (PGO)
```
clang -O2 -fprofile-instr-generate app.c -o app && ./app <representative workload>
llvm-profdata merge -output=app.profdata default.profraw
clang -O2 -fprofile-instr-use=app.profdata app.c -o app
```
GCC: `-fprofile-generate` / `-fprofile-use`. Often 10-20% for branchy code (compilers, interpreters,
databases). Rust: `cargo pgo`; Go 1.21+: `default.pgo` profile in the main package; .NET has Dynamic
PGO on by default. Post-link optimisers (BOLT) add more for large binaries.

## Keep observability
`-fno-omit-frame-pointer` (and `-mno-omit-leaf-frame-pointer`) costs ~1% and makes profilers and eBPF
stack walking reliable; Fedora and Ubuntu now build with it. Always keep `-g` for symbols (separate
debug files) even in release.

## Safety flags that interact
`-D_FORTIFY_SOURCE=3`, `-fstack-protector-strong`, `-fstack-clash-protection`, `-fcf-protection`
(hardening) cost little; keep them.

## Verify
Benchmark each change with statistics (multiple runs, CI); check that hot functions were actually
vectorised/inlined (`-fopt-info-vec`, `-Rpass=loop-vectorize`, Compiler Explorer).
