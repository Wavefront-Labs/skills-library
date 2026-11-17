---
id: computing-software.firmware-embedded-development.platformio.pio-check-static-analysis
name: pio-check-static-analysis
category: computing-software
field: firmware-embedded-development
product: platformio
tags: [pio-ci, pio-check, cppcheck, clang-tidy, pvs-studio, check-flags, check-skip-packages, fail-on-defect, platformio, check-tool, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Run static analysis on firmware with pio check (cppcheck, clang-tidy): check_tool, check_flags, severity and source filters, skipping framework code, MISRA addon, CI gating."
sources:
  - https://docs.platformio.org/en/latest/advanced/static-code-analysis/index.html
  - https://docs.platformio.org/en/latest/advanced/static-code-analysis/tools/cppcheck.html
  - https://docs.platformio.org/en/latest/advanced/static-code-analysis/tools/clang-tidy.html
  - https://docs.platformio.org/en/latest/core/userguide/cmd_check.html
  - https://docs.platformio.org/en/latest/projectconf/sections/env/options/check/index.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Static analysis with pio check

**Goal:** catch bugs on every commit, analysing only your code with the project's real defines
and includes.

## Configuration
```ini
[env:board]
check_tool = cppcheck, clangtidy          ; default is cppcheck
check_flags =
    cppcheck: --enable=performance --inline-suppr
    clangtidy: --checks=-*,bugprone-*,clang-analyzer-*
check_skip_packages = yes                 ; exclude third-party packages (default no)
check_src_filters =
    +<src/>
    -<src/vendor_blob/>
check_severity = medium, high             ; default is low, medium, high
```
- `check_flags` apply to all tools by default; prefix a line with the tool name and a colon to
  target one tool. `pio check --flags` is the command-line equivalent.
- `check_src_filters` uses `+<PATH>` and `-<PATH>` templates (globs allowed, applied in order,
  paths relative to the source directory). By default all files in the `src` and `include`
  folders are included.
- `check_skip_packages` excludes frameworks and toolchains from analysis. By default PlatformIO
  passes their include paths to the tools so project sources parse correctly; some tools use their
  own preprocessor that may fail on valid code and give empty or partial reports.
- Severity: `high` (issues that are possibly bugs), `medium` (defensive-programming suggestions),
  `low` (cleanup and performance such as unused functions and redundant code).

## Running
`pio check -e board`. Other options: `-f/--src-filters`, `--severity`, `--skip-packages`,
`--json-output`, `-v`. `--fail-on-defect` exits non-zero if a defect of the given severity is
found (repeat it for several levels, for example `--fail-on-defect=low --fail-on-defect=medium`);
by default the exit code is the tool's own.

## Tools
- **cppcheck** (default): `--enable=...`, `--inline-suppr`, `--suppress=<spec>` with
  `[error id]:[filename]:[line]`. MISRA and CERT addons are supported: for MISRA the text of the
  rules is proprietary, so create a rule texts file yourself and pass it through an addon JSON:
  ```json
  { "script": "addons/misra.py", "args": ["--rule-texts=misra-rules.txt"] }
  ```
  then `check_flags = cppcheck: --addon=misra.json`.
- **clang-tidy**: `--checks=<string>` (comma-separated, `*` default), `--fix`, `--fix-errors`,
  `--format-style=<string>`, `--system-headers`.
The documentation covers these two tools.

## Suppressions
- cppcheck inline: `// cppcheck-suppress warningId` on the line before the warning (needs
  `--inline-suppr`, enabled by default when no extra flags are given).
- Prefer fixing the code; suppressions accumulate.

## CI pattern
```yaml
- run: pip install platformio
- run: pio check -e board --fail-on-defect=high
```
Start with the high severity, then tighten.

## Gotchas
- Without `check_skip_packages`, framework sources can dominate the report (or fail to parse).
- Analysis uses the env's `build_flags`; code under `#ifdef` for other envs is not checked: run
  check on each meaningful env.

## Verify
- [ ] `pio check` runs in CI with a defined failure threshold.
- [ ] Introducing an obvious defect makes CI fail.

## Checked
2026-10-26 against platformio-docs (develop, last commit 2026-09-19): static-code-analysis
pages, `pio check` reference and the check option pages. Confirmed: option names, defaults and
syntax, severity meanings, `--fail-on-defect` semantics, cppcheck and clang-tidy flags, MISRA
addon JSON, cppcheck inline suppression. Removed as unconfirmed: PVS-Studio (not in the current
tool list), `--std=c++17`, `--suppressions-list`, `NOLINT` advice, `missingInclude` remarks, the
CERT check list and HTML output upload.
Method: documentation only; no commands were run.
