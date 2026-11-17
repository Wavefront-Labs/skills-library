---
id: computing-software.software-engineering.r.r-debug-tools
name: r-debug-tools
category: computing-software
field: software-engineering
product: r
tags: [r, r-debugging, debug-tools]
level: practitioner
status: docs-checked
description: "Locate failing code with traceback, step with debug and browser, and set options(error=)."
sources: ["https://stat.ethz.ch/R-manual/R-devel/library/base/html/debug.html", "https://stat.ethz.ch/R-manual/R-devel/library/base/html/traceback.html", "https://stat.ethz.ch/R-manual/R-devel/library/base/html/options.html", "https://stat.ethz.ch/R-manual/R-devel/library/utils/html/recover.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# traceback, browser, debug and recover
- `traceback()` shows the call stack after an error.
- `debug(f)` and `undebug(f)` flag and unflag a function for stepping; `debugonce(f)` enters the debugger only the next time it is called.
- `options(error = recover)` makes an error open a frame selector (`?recover`).
- `options(warn = 2)` turns warnings into errors (`?options`).
Verify: Reproduce the error in a minimal example and step through with `debugonce(f)`.

## Checked

Date: 2026-11-02. Confirmed on: ?debug (debugonce), ?traceback, ?recover (options(error = recover)), ?options (warn level that turns warnings into errors). Removed as not confirmed on those pages: rlang::last_trace(), reprex, the Rscript exit-status claim, and the browser() description.

Method: documentation only; no commands were run.
