---
id: computing-software.software-engineering.r.r-base-plot-par
name: r-base-plot-par
category: computing-software
field: software-engineering
product: r
tags: [r, r-base-graphics, base-plot-par]
level: practitioner
status: docs-checked
description: "Make multi-panel base plots with par(mfrow), save with png/pdf and restore par."
sources: ["https://stat.ethz.ch/R-manual/R-devel/library/graphics/html/par.html", "https://stat.ethz.ch/R-manual/R-devel/library/graphics/html/legend.html", "https://stat.ethz.ch/R-manual/R-devel/library/grDevices/html/dev.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# plot, par, layout and graphics devices
- `op <- par(mfrow = c(1, 2)); on.exit(par(op))` saves and restores graphical parameters (the pattern used in the `?par` examples); `mfrow` takes `c(nr, nc)`.
- `legend("topright", ...)` is a valid position keyword.
- `dev.list()` returns the numbers of all open devices; `graphics.off()` shuts down all of them; `dev.off()` closes the current device.
Verify: `dev.list()` is empty after the script finishes.

## Checked

Date: 2026-11-02. Confirmed on: ?par (mfrow, on.exit(par(op)) example), ?legend ("topright"), ?dev (dev.list, graphics.off, dev.off). Removed as not confirmed on those pages: png() size and res arguments, the claim that a forgotten dev.off() leaves the file unfinished, and the plot/hist/boxplot call list (not checked on these pages).

Method: documentation only; no commands were run.
