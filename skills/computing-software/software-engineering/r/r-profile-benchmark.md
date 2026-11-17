---
id: computing-software.software-engineering.r.r-profile-benchmark
name: r-profile-benchmark
category: computing-software
field: software-engineering
product: r
tags: [r, r-performance, profile-benchmark]
level: advanced
status: draft
description: "Find hot spots with profvis and compare alternatives with bench::mark before optimising."
sources: ["https://cran.r-project.org/manuals.html", ""]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Rprof, profvis and bench
- `profvis::profvis({ ... })` shows line-level time and memory; `Rprof("p.out"); ...; Rprof(NULL); summaryRprof("p.out")`.
- `bench::mark(a = f(x), b = g(x))` checks results are equal and reports time and allocations; `system.time` is coarse.
- Typical wins: vectorise, preallocate, avoid growing objects in loops, avoid repeated `rbind`, use matrices for numeric loops, `data.table` for large aggregates, move loops to Rcpp.
Verify: re-profile after the change.
