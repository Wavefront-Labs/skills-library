---
id: computing-software.software-engineering.r.r-seq-rep-vector-construction
name: r-seq-rep-vector-construction
category: computing-software
field: software-engineering
product: r
tags: [r, seq-rep-vector-construction]
level: practitioner
status: docs-checked
description: "Construct R vectors with seq, seq_len, seq_along, rep, vector() and named vectors."
sources: ["https://stat.ethz.ch/R-manual/R-devel/library/base/html/seq.html", "https://stat.ethz.ch/R-manual/R-devel/library/base/html/rep.html", "https://stat.ethz.ch/R-manual/R-devel/library/base/html/vector.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Building vectors
- `seq_len(n)` and `seq_along(x)` are fast primitives for the common cases (`?seq`) and are empty-safe where `1:length(x)` is not.
- `rep` takes `times`, `each` and `length.out` (`?rep`).
- `vector("list", n)` creates a list of length n (`?vector`).
Verify: `for (i in seq_along(NULL))` does not run.

## Checked

Date: 2026-11-02. Confirmed on: ?seq, ?rep, ?vector. Removed as not confirmed on those pages: The seq(by/length.out) examples, setNames and character(5) lines (not read on these pages).

Method: documentation only; no commands were run.
