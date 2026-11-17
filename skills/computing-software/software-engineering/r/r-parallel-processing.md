---
id: computing-software.software-engineering.r.r-parallel-processing
name: r-parallel-processing
category: computing-software
field: software-engineering
product: r
tags: [r, r-parallel, parallel-processing]
level: advanced
status: docs-checked
description: "Run embarrassingly parallel work with parallel or future and handle Windows and RNG differences."
sources: ["https://stat.ethz.ch/R-manual/R-devel/library/parallel/html/detectCores.html", "https://stat.ethz.ch/R-manual/R-devel/library/parallel/html/clusterApply.html", "https://stat.ethz.ch/R-manual/R-devel/library/parallel/html/makeCluster.html", "https://stat.ethz.ch/R-manual/R-devel/library/parallel/html/RngStream.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# mclapply, parLapply and future
- `detectCores(all.tests = FALSE, logical = TRUE)` counts cores; pass `logical = FALSE` for physical cores where supported (`?detectCores`).
- `makeCluster()` creates a cluster and `stopCluster(cl)` shuts it down (`?makeCluster`); `parLapply` and `clusterExport(cl, varlist)` are on `?clusterApply`.
- The `"L'Ecuyer-CMRG"` generator is used for parallel random streams (`?RngStream`).
Verify: Compare parallel and serial results with `all.equal`.

## Checked

Date: 2026-11-02. Confirmed on: ?detectCores, ?makeCluster, ?clusterApply, ?RngStream. Removed as not confirmed on those pages: mclapply fork behaviour on Windows, and all future/furrr claims (not read on these pages).

Method: documentation only; no commands were run.
