---
id: computing-software.software-engineering.r.r-rcpp-integration
name: r-rcpp-integration
category: computing-software
field: software-engineering
product: r
tags: [r, r-compiled, rcpp-integration]
level: advanced
status: draft
description: "Write C++ with Rcpp::sourceCpp or package Rcpp attributes and respect memory and NA rules."
sources: ["https://cran.r-project.org/manuals.html", ""]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Rcpp functions and compiled code
- `Rcpp::cppFunction("double f(double x) { return x*x; }")` for quick tests; in packages use `// [[Rcpp::export]]`, `Rcpp::compileAttributes()` and `LinkingTo: Rcpp`.
- Vectors are zero-indexed; `NumericVector` shares memory with R, so modifying an argument modifies the caller's object; use `clone()`.
- Integer NA is `NA_INTEGER`; double NA is a NaN with a payload, test with `R_IsNA`.
- Suspected memory errors: run under Valgrind or AddressSanitizer.
Verify: compare the C++ output with the pure R version on random inputs.
