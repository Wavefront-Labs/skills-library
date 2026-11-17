---
id: computing-software.software-engineering.r.r-package-structure
name: r-package-structure
category: computing-software
field: software-engineering
product: r
tags: [r, r-packages, package-structure]
level: practitioner
status: draft
description: "Create a package with usethis, document with roxygen2 and manage Imports and exports."
sources: ["https://cran.r-project.org/manuals.html", ""]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# DESCRIPTION, NAMESPACE and roxygen2
- `usethis::create_package()`, `use_r("name")`, `use_test()`, `use_mit_license()`, `use_git()`.
- `DESCRIPTION` has `Imports` (needed at runtime) and `Suggests` (tests, vignettes); call functions as `pkg::fn()` or `@importFrom`.
- roxygen2: `#' @param`, `#' @return`, `#' @export`, `#' @examples`; run `devtools::document()` to generate `NAMESPACE` and `man/`.
- `devtools::load_all()` during development; never call `library()` or `require()` inside package code.
Verify: `devtools::check()` returns 0 errors, 0 warnings.
