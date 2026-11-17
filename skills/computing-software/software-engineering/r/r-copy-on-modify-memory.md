---
id: computing-software.software-engineering.r.r-copy-on-modify-memory
name: r-copy-on-modify-memory
category: computing-software
field: software-engineering
product: r
tags: [r, r-memory, copy-on-modify-memory]
level: advanced
status: docs-checked
description: "Understand when R copies objects and check memory with lobstr and gc."
sources: ["https://stat.ethz.ch/R-manual/R-devel/library/base/html/tracemem.html", "https://stat.ethz.ch/R-manual/R-devel/library/base/html/gc.html", "https://stat.ethz.ch/R-manual/R-devel/library/utils/html/object.size.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Copy-on-modify, gc and object size
- `tracemem(x)` marks an object so that copies of it are reported; it is documented on `?tracemem`.
- `gc()` runs a garbage collection and reports memory use (`?gc`); explicit calls are rarely needed.
- `utils::object.size(x)` estimates the memory an object uses (`?object.size`).
Verify: `tracemem(x)` prints a line when the object is copied.

## Checked

Date: 2026-11-02. Confirmed on: ?tracemem, ?gc and ?object.size exist and describe these functions. Removed as not confirmed on those pages: The lobstr claims, copy-on-modify behaviour inside loops, and the Arrow/duckdb advice (outside these pages).

Method: documentation only; no commands were run.
