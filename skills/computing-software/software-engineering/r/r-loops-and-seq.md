---
id: computing-software.software-engineering.r.r-loops-and-seq
name: r-loops-and-seq
category: computing-software
field: software-engineering
product: r
tags: [r, r-control-flow, loops-and-seq]
level: practitioner
status: docs-checked
description: "Write correct and fast for loops with seq_along, preallocated results and break/next."
sources: ["https://stat.ethz.ch/R-manual/R-devel/library/base/html/seq.html", "https://stat.ethz.ch/R-manual/R-devel/library/base/html/system.time.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Loops, seq_along and preallocation
- `seq_len` and `seq_along` are fast primitives for the two common cases (`?seq`); prefer them to `1:length(x)`, which iterates 1, 0 for empty input.
- Preallocate the result (`numeric(n)`, `vector("list", n)`) and assign `out[i] <- ...` rather than growing it.
- `system.time()` measures a timed expression.
Verify: Time the loop against the vectorised form with `system.time()`.

## Checked

Date: 2026-11-02. Confirmed on: ?seq (seq_len, seq_along), ?system.time. Removed as not confirmed on those pages: The Date-class stripping claim in for loops and the retry-loop advice (not read on these pages).

Method: documentation only; no commands were run.
