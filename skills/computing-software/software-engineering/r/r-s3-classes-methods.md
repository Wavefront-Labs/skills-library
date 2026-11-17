---
id: computing-software.software-engineering.r.r-s3-classes-methods
name: r-s3-classes-methods
category: computing-software
field: software-engineering
product: r
tags: [r, r-oop-s3, s3-classes-methods]
level: advanced
status: docs-checked
description: "Define constructors, validators, generics with UseMethod and registered methods."
sources: ["https://stat.ethz.ch/R-manual/R-devel/library/base/html/UseMethod.html", "https://stat.ethz.ch/R-manual/R-devel/library/base/html/class.html", "https://stat.ethz.ch/R-manual/R-devel/library/utils/html/getS3method.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Writing S3 classes, generics and methods
- A generic is a function that calls `UseMethod("area")`; methods are named `area.circle`, with `area.default` as the fallback (`?UseMethod`).
- `NextMethod()` calls the next method in the class vector (`?UseMethod`).
- If there is no class attribute, the implicit class is tried when dispatching (`?class`).
- `inherits(x, what, which = FALSE)` tests class membership (`?class`); `getS3method("area", "circle")` returns a registered method (`?getS3method`).
Verify: `getS3method("area", "circle")` returns the method.

## Checked

Date: 2026-11-02. Confirmed on: ?UseMethod (UseMethod, NextMethod), ?class (implicit class, inherits), ?getS3method. Removed as not confirmed on those pages: NAMESPACE S3method registration, constructor/validator conventions, and the print/format/summary advice (not read on these pages).

Method: documentation only; no commands were run.
