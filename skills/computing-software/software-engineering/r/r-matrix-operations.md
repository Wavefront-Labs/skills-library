---
id: computing-software.software-engineering.r.r-matrix-operations
name: r-matrix-operations
category: computing-software
field: software-engineering
product: r
tags: [r, r-matrices, matrix-operations]
level: practitioner
status: docs-checked
description: "Build matrices, use %*% and solve, apply over margins and avoid dimension dropping."
sources: ["https://stat.ethz.ch/R-manual/R-devel/library/base/html/matrix.html", "https://stat.ethz.ch/R-manual/R-devel/library/base/html/crossprod.html", "https://stat.ethz.ch/R-manual/R-devel/library/base/html/solve.html", "https://stat.ethz.ch/R-manual/R-devel/library/base/html/colSums.html", "https://stat.ethz.ch/R-manual/R-devel/library/base/html/Extract.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Matrix creation, apply and linear algebra
- `matrix(data, nrow, ncol, byrow = FALSE)`: the matrix is filled by column unless `byrow = TRUE`.
- `crossprod(x)` is the cross product (`?crossprod`); `solve(a, b)` solves `a %*% x = b` for `x` (`?solve`).
- `m[1, , drop = FALSE]` keeps a one-row matrix (`?Extract`).
- `rowSums` and `colSums`, `rowMeans` and `colMeans` are documented together on `?colSums`.
Verify: `all.equal(A %*% solve(A), diag(n))`.

## Checked

Date: 2026-11-02. Confirmed on: ?matrix (byrow), ?crossprod, ?solve, ?Extract (drop = FALSE), ?colSums. Removed as not confirmed on those pages: The speed claims (crossprod versus t(x) %*% x, rowSums versus apply), the Matrix package advice, and the qr/chol/svd/eigen list (not read on these pages).

Method: documentation only; no commands were run.
