---
id: computing-software.software-engineering.cpp.clang-format-and-include-what-you-use
name: clang-format-and-include-what-you-use
category: computing-software
field: software-engineering
product: cpp
tags: [cpp, cpp-testing, clang-format, include-what-you-use, clang-tidy, code-style, include-hygiene, cpp-style]
level: practitioner
status: docs-checked
description: "Enforce C++ formatting with clang-format and include hygiene with include-what-you-use and clang-tidy, in editors, pre-commit hooks and CI without churn."
sources:
  - https://clang.llvm.org/docs/ClangFormat.html
  - https://clang.llvm.org/docs/ClangFormatStyleOptions.html
  - https://github.com/include-what-you-use/include-what-you-use
  - https://clang.llvm.org/extra/clang-tidy/
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# clang-format and include hygiene

**Goal:** consistent formatting with zero review discussion, and each file including exactly what it uses.

## 1. clang-format configuration
```yaml
# .clang-format
BasedOnStyle: Google          # or LLVM, Chromium, Mozilla, WebKit, Microsoft, GNU
Language: Cpp
Standard: c++20
ColumnLimit: 100
IndentWidth: 4
PointerAlignment: Left
IncludeBlocks: Regroup
IncludeCategories:
  - { Regex: '^<[a-z_]+>$',      Priority: 1 }   # C++ standard headers
  - { Regex: '^<.*\.h>$',        Priority: 2 }   # C/system headers
  - { Regex: '^<.*>$',           Priority: 3 }   # third-party
  - { Regex: '.*',               Priority: 4 }   # project
InsertBraces: true
```
```bash
clang-format -i $(git ls-files '*.cpp' '*.h' '*.hpp')
clang-format --dry-run --Werror file.cpp       # CI check
git clang-format origin/main                   # format only changed lines (legacy codebases)
```
Use the same clang-format version for everyone (a pinned package or container) so output does not drift between releases; the options available depend on the version (for example `InsertBraces` needs clang-format 15).
Escape hatch: `// clang-format off` ... `// clang-format on` for tables and matrices.

## 2. Rollout
One mass-format commit recorded in an ignore-revs file for `git blame`; editors format on save; a pre-commit hook; CI check.

## 3. include-what-you-use (IWYU)
Each file should directly include headers for the symbols it uses, and nothing else. Benefits: faster builds, no breakage when a transitive include disappears.
```bash
cmake -B build -DCMAKE_EXPORT_COMPILE_COMMANDS=ON
iwyu_tool.py -p build -- -Xiwyu --mapping_file=iwyu.imp > iwyu.out
fix_includes.py < iwyu.out
# or per build: set(CMAKE_CXX_INCLUDE_WHAT_YOU_USE include-what-you-use)
```
Mapping files (`.imp`) teach IWYU about umbrella headers and private headers of third-party libraries. Use `// IWYU pragma: keep` / `export` for intentional exceptions. Review its suggestions; it is right most of the time, not always.

## 4. clang-tidy complements
```yaml
# .clang-tidy
Checks: >
  -*,bugprone-*,cert-*,cppcoreguidelines-*,misc-include-cleaner,modernize-*,performance-*,readability-*,
  -modernize-use-trailing-return-type,-readability-magic-numbers
WarningsAsErrors: 'bugprone-*'
HeaderFilterRegex: '^src/'
```
`misc-include-cleaner` (which follows clangd's Include Cleaner) and clangd's unused-include diagnostics give IWYU-like checks in the editor. Run `run-clang-tidy.py -p build` in CI, or `clang-tidy-diff.py` on changed lines.

## Gotchas
- clang-format can reorder includes and break code that depends on include order; fix the headers (make them self-contained) rather than disabling sorting.
- Formatting macros and DSL-like code may look worse; accept or fence with off/on.
- IWYU needs the same compile flags as the build; compile_commands.json is required.

## Verify
- `clang-format --dry-run --Werror` passes in CI on all files, each header compiles on its own (a CI target that includes each header in an empty .cpp), and IWYU reports no changes on the main targets.

## Checked

Date: 2026-10-25. Documentation: LLVM project docs (llvm/llvm-project clang/docs ClangFormat.md and ClangFormatStyleOptions.md, clang-tools-extra clang-tidy index and misc-include-cleaner, repository head 2026-10-25) and the include-what-you-use repository README and docs (head 2026-10-24).

Confirmed: BasedOnStyle values (LLVM, Google, Chromium, Mozilla, WebKit, Microsoft, GNU); `IncludeBlocks: Regroup` and `IncludeCategories` Priority; `Standard` accepts `c++20`; `InsertBraces` (clang-format 15); `--dry-run`, `--Werror`, `git clang-format`; `// clang-format off` and `on`; `iwyu_tool.py -p`, `fix_includes.py`, `-Xiwyu --mapping_file`, `CMAKE_CXX_INCLUDE_WHAT_YOU_USE`, `IWYU pragma: keep` and `export`; clang-tidy `run-clang-tidy.py`, `clang-tidy-diff.py`, `HeaderFilterRegex`, `WarningsAsErrors`.
Removed as unconfirmed: the pip version pin, the pre-commit mirror name, the `--nosafe_headers` flag, and the clang-tidy 17 version gate.

Method: documentation only; no commands were run.
