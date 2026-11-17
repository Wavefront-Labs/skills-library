---
id: computing-software.software-engineering.r.r-seed-and-sampling
name: r-seed-and-sampling
category: computing-software
field: software-engineering
product: r
tags: [r, r-random, seed-and-sampling]
level: practitioner
status: docs-checked
description: "Make simulations reproducible with set.seed and avoid sample() on a single number."
sources: ["https://stat.ethz.ch/R-manual/R-devel/library/base/html/sample.html", "https://stat.ethz.ch/R-manual/R-devel/library/parallel/html/RngStream.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# set.seed, sample and RNG kinds
- `sample.int(n, size = n, replace = FALSE, prob = NULL)` is the integer form; in `sample(x)` the argument `n` is a positive number of items to choose from (`?sample`).
- For parallel streams, the parallel package uses the `"L'Ecuyer-CMRG"` generator (`?RngStream`, `?parallel-package`).
Verify: Two runs with the same seed give `identical()` output.

## Checked

Date: 2026-11-02. Confirmed on: ?sample (sample.int signature), ?RngStream and the parallel package overview (L'Ecuyer-CMRG). Removed as not confirmed on those pages: The R 3.6.0 sample.kind change, the length-one x trap, and distribution-argument-order remark (not read on these pages).

Method: documentation only; no commands were run.
