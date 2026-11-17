---
id: computing-software.software-engineering.r.r-s4-classes
name: r-s4-classes
category: computing-software
field: software-engineering
product: r
tags: [r, r-oop-s4, s4-classes]
level: advanced
status: docs-checked
description: "Use setClass, validity, setGeneric, setMethod and show methods."
sources: ["https://stat.ethz.ch/R-manual/R-devel/library/methods/html/setClass.html", "https://stat.ethz.ch/R-manual/R-devel/library/methods/html/validObject.html", "https://stat.ethz.ch/R-manual/R-devel/library/methods/html/showMethods.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# S4 classes, generics and validity
- `setClass(Class, representation, prototype, contains = character(), ...)` defines a class (`?setClass`).
- `setValidity(Class, method)` registers a validity method; `validObject()` runs it (`?validObject`).
- `showMethods` lists the methods of a generic (`?showMethods`).
Verify: `showMethods("area")` lists the expected methods.

## Checked

Date: 2026-11-02. Confirmed on: ?setClass (representation, prototype arguments), ?validObject (setValidity), ?showMethods. Removed as not confirmed on those pages: The setGeneric/setMethod forms, callNextMethod, isVirtualClass and slot access claims (not read on these pages).

Method: documentation only; no commands were run.
