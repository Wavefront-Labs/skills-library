---
id: computing-software.software-engineering.compiler-construction.lto-and-pgo
name: lto-and-pgo
category: computing-software
field: software-engineering
product: compiler-construction
tags: [compiler-construction, thin-lto, profile-guided-optimization, instrumentation-profile, lto, pgo, sanitizers-instrumentation, compilers, interpreters, language-implementation]
level: practitioner
status: docs-checked
description: "Release builds"
sources:
  - https://clang.llvm.org/docs/ThinLTO.html
  - https://clang.llvm.org/docs/UsersManual.html
  - https://llvm.org/docs/CommandGuide/llvm-profdata.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# LTO and PGO

Goal: use whole-program information.
- ThinLTO: add `-flto=thin` at compile and link (for example `clang -flto=thin -O2 file1.c file2.c -c`, then link the objects). Clang emits bitcode with a module summary; the link step merges summaries and function importing happens in parallel backends, so it scales and stays incremental unlike monolithic LTO.
- Instrumented PGO: build with `-fprofile-generate` (or `-fprofile-instr-generate`), run the program, merge with `llvm-profdata merge -output=code.profdata <raw profiles>`, then rebuild with `-fprofile-use=code.profdata` (or `-fprofile-instr-use`).
- Profile data from one kind of instrumentation cannot be used by the other, so pair `-fprofile-generate` with `-fprofile-use`, and `-fprofile-instr-generate` with `-fprofile-instr-use`.
- Profiles help block ordering and the inliner; `-O2` or above is recommended.
Verify: benchmarks show gains.

## Checked
2026-11-08. Confirmed in the Clang ThinLTO page, the Clang Users Manual profile-guided optimization section and the llvm-profdata merge page. Removed: refresh-regularly and mismatch-warning advice, branch-weight wording, and the BOLT remark (not on these pages).
Method: documentation only; no commands were run.
