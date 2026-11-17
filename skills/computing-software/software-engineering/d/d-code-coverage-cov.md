---
id: computing-software.software-engineering.d.d-code-coverage-cov
name: d-code-coverage-cov
category: computing-software
field: software-engineering
product: d
tags: [d-code-coverage-cov, unit-tests, -cov, coverage, lst-files, unittest-cov, dub-test-coverage, lcov, d]
level: practitioner
status: draft
description: "Measure coverage with dmd -cov (or dub -b unittest-cov), read the generated .lst files, set -cov=percent thresholds, and merge or reset counts."
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

# Code coverage with -cov and .lst files

Goal: see which lines tests execute.

- Compile with `-cov` (and `-unittest`): `dmd -cov -unittest -main -run mod.d`. At exit, `<module>.lst` files list execution counts per line, with `|` for non-executable and `0000000|` for unexecuted lines; the last line shows `mod.d is 87% covered`.
- Fail under a threshold: `-cov=90` makes the run fail if coverage is under 90% (confirm exact semantic with your version).
- dub: `dub test --coverage` (also `-b unittest-cov`); lst files go to the project dir or `.dub`; clean them from VCS with `*.lst` in `.gitignore`.
- LDC: `ldc2 -cov`; use `--d-debug` for debug lines. LDC can also emit LLVM coverage (`-fprofile-instr-generate`, confirm).
- Custom runner: `core.runtime.dmd_coverSetMerge(true)` merges counts across runs; `dmd_coverDestPath("dir")` sets the output directory; `dmd_coverSourcePath`.
- Convert to Cobertura/lcov with community tools (`dub fetch d-cov`-style converters, confirm package names).

Gotchas:
- Coverage counts lines, not branches.
- Templates are counted per instantiation; uninstantiated code shows 0000000.

Verify: run twice with merge enabled and see counts grow.
