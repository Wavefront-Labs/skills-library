---
id: computing-software.software-engineering.deno.coverage-collect-and-report
name: coverage-collect-and-report
category: computing-software
field: software-engineering
product: deno
tags: [coverage, deno-coverage, v8, lcov, html-report, subprocess-coverage]
level: practitioner
status: docs-checked
description: "Collect V8 coverage with deno test --coverage (or deno run), read summary and --detailed reports, generate HTML and lcov, and gather subprocess coverage."
sources:
  - https://raw.githubusercontent.com/denoland/docs/main/runtime/test/coverage.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Two steps: collect, then report.

```sh
deno test --coverage                 # raw V8 profiles into coverage/
deno test --coverage=cov_profile     # custom dir (or DENO_COVERAGE_DIR)
deno test --clean --coverage         # empty the dir first; stale profiles skew results
```

Deno also prints a summary table and writes `lcov.info` and an HTML report in the directory. `--coverage-raw-data-only` keeps only raw profiles.

Measure code outside the test runner:

```sh
deno run --coverage=cov_profile main.ts
```

For tests that spawn Deno subprocesses, set `DENO_COVERAGE_DIR` (children inherit it):

```sh
DENO_COVERAGE_DIR=cov_profile deno test --allow-run
deno coverage cov_profile
```

Reports:

```sh
deno coverage coverage/              # Branch %, Function %, Line % per file
deno coverage --detailed coverage/   # lists uncovered lines
deno coverage --html coverage/       # writes coverage/html/index.html
deno coverage --lcov --output=coverage.lcov coverage/
```

Without `--output`, lcov goes to stdout. In GitHub Actions: `deno test --coverage`, then the lcov command, then `codecov/codecov-action@v5` with `files: coverage.lcov`.

`deno coverage` has no built-in threshold flag. Either gate in your coverage service, or sum `LF` (lines found) and `LH` (lines hit) from the lcov file in CI.

## Checked

2026-11-04. Confirmed against docs runtime/test/coverage.md: --coverage, custom dir and DENO_COVERAGE_DIR, --clean, --coverage-raw-data-only, deno run --coverage, --detailed, --html, --lcov --output, codecov action v5, no threshold flag.

Method: documentation only; no commands were run.
