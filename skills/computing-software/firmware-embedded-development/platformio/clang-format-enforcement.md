---
id: computing-software.firmware-embedded-development.platformio.clang-format-enforcement
name: clang-format-enforcement
category: computing-software
field: firmware-embedded-development
product: platformio
tags: [clang-format, code-formatting, pre-commit, format-check-ci, clang-format-file, vendor-code-exclusion, platformio, firmware-embedded-development]
level: practitioner
status: draft
description: "Enforce clang-format on firmware repos: .clang-format for embedded C/C++, excluding vendor code, pinned versions, pre-commit hooks, CI --dry-run --Werror checks."
sources:
  - https://clang.llvm.org/docs/ClangFormatStyleOptions.html
  - https://clang.llvm.org/docs/ClangFormat.html
  - https://github.com/pre-commit/mirrors-clang-format
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# clang-format enforcement

## Config
```yaml
# .clang-format
BasedOnStyle: LLVM
IndentWidth: 4
ColumnLimit: 100
BreakBeforeBraces: Linux
AllowShortFunctionsOnASingleLine: Empty
AllowShortIfStatementsOnASingleLine: Never
PointerAlignment: Right
SortIncludes: false           # include order matters in some vendor/HAL headers
AlignConsecutiveMacros: Consecutive
AlignConsecutiveAssignments: None
SpaceAfterCStyleCast: true
IndentCaseLabels: false
```
Turn formatting off for tables and register maps that must stay aligned:
```c
// clang-format off
static const uint8_t lut[] = { 0x00, 0x07, 0x0E, 0x09,
                               0x1C, 0x1B, 0x12, 0x15 };
// clang-format on
```

## Exclude vendor code
Never reformat CubeMX/HAL/CMSIS/SDK files (diffs explode on regeneration). Options:
- Put `DisableFormat: true` in a `.clang-format` inside vendor directories (`lib/vendor/`,
  `Drivers/`).
- Build the file list from your own folders only (`src/`, `include/`, `lib/app_*`, `test/`).
- `.clang-format-ignore` (clang-format 18+) with glob patterns.

## Pin the version
Different clang-format majors format differently. Pin it: `pip install clang-format==18.1.8`
(PyPI wheels), or the pre-commit mirror with a fixed `rev`.

## Pre-commit hook
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/pre-commit/mirrors-clang-format
    rev: v18.1.8
    hooks:
      - id: clang-format
        types_or: [c, c++]
        exclude: ^(lib/vendor|Drivers)/
```
`pre-commit install` once per clone.

## CI check
```sh
git ls-files 'src/*.c' 'src/*.h' 'src/*.cpp' 'include/*.h' 'test/*.c*' \
  | xargs clang-format --dry-run --Werror
```
Run it as a separate fast job before `pio run`. `--dry-run --Werror` exits non-zero and prints
diffs-as-warnings; no files are modified.

## Editor
VS Code C/C++ extension: `"C_Cpp.clang_format_style": "file"`, `"editor.formatOnSave": true`, and
point `"C_Cpp.clang_format_path"` at the pinned binary so editor and CI agree.

## Rolling out
Format the whole codebase in one dedicated commit and add its hash to `.git-blame-ignore-revs`
(`git config blame.ignoreRevsFile .git-blame-ignore-revs`) so blame stays useful.

## Verify
- [ ] CI fails on an unformatted change and passes after `clang-format -i`.
- [ ] Vendor directories untouched by a full-repo format run.
