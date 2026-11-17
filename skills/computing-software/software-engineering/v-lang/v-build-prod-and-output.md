---
id: computing-software.software-engineering.v-lang.v-build-prod-and-output
name: v-build-prod-and-output
category: computing-software
field: software-engineering
product: v-lang
tags: [v-build-prod-and-output, v-cli-run-and-build, prod, cflags, compress, optimise, release-build, build-flags, v-lang]
level: practitioner
status: docs-checked
description: "V build flags per the language docs: -prod effects, -cc, -cflags and -ldflags, -compress via upx, -march=native trade-offs, -showcc and -keepc for inspecting generated C."
sources:
  - https://raw.githubusercontent.com/vlang/v/master/doc/docs.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# v build flags: -prod, -cc, -cflags, -compress

Goal: ship small, fast executables, tuning only after profiling.

- `-prod` enables production mode: unused variables become an error (they are only a warning otherwise), all `assert` statements are removed, and deprecated-function warnings become errors. With `-prod` the generated C usually performs well.
- The docs say further tuning is rarely needed and should follow profiling. Their table: `@[inline]` (performance, bigger binary), `@[direct_array_access]` (performance, safety risk), `@[packed]` (memory), `@[minify]`, `-fast-math` (risk of incorrect results), `-d no_segfault_handler` (smaller and faster to compile, loses segfault trace), `-cflags -march=native` (faster, but incompatible with other or older CPUs), `-compress` (smaller), and PGO.
- `-compress` runs `upx` on the result, reducing size by around 50-70%; it starts a bit slower, uses extra RAM initially, is harder to debug and some antivirus heuristics trigger more often.
- `-cc <compiler>` selects the C compiler (docs examples: gcc, clang, msvc). `-cflags` passes flags to the backend C compiler (before other C options); `-ldflags` passes flags to the C linker (after every other option). Example: `-cc gcc-9 -cflags -fsanitize=thread`.
- PGO example from the docs: `v -cc clang -prod -cflags -fprofile-generate -o pgo_gen .` then `-cflags "-fprofile-use=..."`.
- Inspect the build: `-showcc` prints the C compiler command, `-show-c-output` prints the C compiler's output, `-keepc` keeps the generated C file at a stable path.

Verify: compare binary size and timing for `v .` against `v -prod .`.

## Checked
2026-11-08. Checked against the V documentation (`doc/docs.md`): production mode, performance tuning table, `-compress`, `-march=native`, `-cc`/`-cflags`/`-ldflags`, PGO and the debugging flags. Removed (not stated there, or not checked): the claim that tcc is dev-only, `-skip-unused` default status, `-d no_backtrace`, `strip`, static linking with musl-gcc, writing C with `-o out.c`, and the bounds/overflow-check gotcha. `-keep-c` corrected to the documented spelling `-keepc`. Replaced landing-page sources with the raw docs file.
Method: documentation only; no commands were run.
