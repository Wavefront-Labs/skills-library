---
id: computing-software.software-engineering.r.r-s3-methods-inheritance-nextmethod
name: r-s3-methods-inheritance-nextmethod
category: computing-software
field: software-engineering
product: r
tags: [r, s3-methods-inheritance-nextmethod]
level: advanced
status: docs-checked
description: "Define S3 classes in R: constructors/validators, UseMethod dispatch, inherits, NextMethod and print/format methods."
sources: ["https://stat.ethz.ch/R-manual/R-devel/library/base/html/UseMethod.html", "https://stat.ethz.ch/R-manual/R-devel/library/base/html/class.html", "https://stat.ethz.ch/R-manual/R-devel/library/base/html/groupGeneric.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# S3
- Set a class vector with `structure(list(v = v), class = c("child", "parent"))`; dispatch walks the vector, and `NextMethod()` calls the next method (`?UseMethod`).
- `area <- function(x, ...) UseMethod("area")` defines a generic; `area.default` is the fallback.
- `inherits(x, "parent")` tests class membership (`?class`).
- Group generics such as `Ops` are documented on `?groupGeneric`.
Verify: `print(obj)` dispatches to `print.child`.

## Checked

Date: 2026-11-02. Confirmed on: ?UseMethod, ?class, ?groupGeneric. Removed as not confirmed on those pages: NAMESPACE registration advice, unclass(), and methods() usage (not read on these pages).

Method: documentation only; no commands were run.
