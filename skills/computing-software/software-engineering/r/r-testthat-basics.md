---
id: computing-software.software-engineering.r.r-testthat-basics
name: r-testthat-basics
category: computing-software
field: software-engineering
product: r
tags: [r, r-testing, testthat-basics]
level: practitioner
status: draft
description: "Write testthat 3e tests with expect_* functions, test fixtures, mocking and snapshot tests."
sources: ["https://cran.r-project.org/manuals.html", ""]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# testthat expectations, fixtures and snapshots
- Enable the third edition with `Config/testthat/edition: 3` in DESCRIPTION; tests live in `tests/testthat/test-*.R`.
- `expect_equal(a, b)` (tolerance for numerics), `expect_identical`, `expect_error(f(), "regex")`, `expect_snapshot()` for output.
- `withr::local_tempfile()` and `withr::local_options()` clean up after tests; `skip_on_cran()`, `skip_if_not_installed()`.
- `testthat::local_mocked_bindings()` replaces functions (testthat 3.2.0 or newer).
- Run with `devtools::test()`; `covr::package_coverage()` for coverage.
Verify: a deliberately broken function should fail the suite.
