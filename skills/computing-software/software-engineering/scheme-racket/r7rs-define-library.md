---
id: computing-software.software-engineering.scheme-racket.r7rs-define-library
name: r7rs-define-library
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, r7rs-define-library, r7rs-small]
level: advanced
status: docs-checked
description: "Write portable R7RS-small libraries with define-library, export, import, begin and include, and know the standard (scheme ...) library names."
sources:
  - https://small.r7rs.org/attachment/r7rs.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# R7RS define-library and import
**Goal:** portable Scheme libraries.
```scheme
(define-library (my lib)
  (export double)
  (import (scheme base))
  (begin (define (double x) (* 2 x))))
```
- A library name is a list of identifiers and exact non-negative integers. Names starting with `scheme` are reserved for the report, and names starting with `srfi` for SRFI libraries.
- Declarations are `export`, `import`, `begin`, `include`, `include-ci`, `include-library-declarations` and `cond-expand`. An export spec is an identifier or `(rename internal external)`.
- `begin`, `include` and `include-ci` give the library body; `include-library-declarations` splices a file's declarations into the library (for example to share one export list).
- Standard libraries in Appendix A: `(scheme base)`, `(scheme case-lambda)`, `(scheme char)`, `(scheme complex)`, `(scheme cxr)`, `(scheme eval)`, `(scheme file)`, `(scheme inexact)`, `(scheme lazy)`, `(scheme load)`, `(scheme process-context)`, `(scheme read)`, `(scheme repl)`, `(scheme time)`, `(scheme write)`, `(scheme r5rs)`.
- Several `import` declarations of one library are equivalent to a single combined one.
## Self-check
Import `(scheme base)` and `(scheme write)` and print with `display` (`display` is exported by `(scheme write)`).
## Checked
2026-11-08. Confirmed in the R7RS-small report, section 5.6 (Libraries) and Appendix A (Standard Libraries): library name rules, the declaration list, export specs, include semantics, and the list of standard libraries including `display` in `(scheme write)`. Removed: the Racket-specific claims (`r7rs` package install, `#lang r7rs`) because the Racket r7rs documentation page was not readable; `(scheme repl)` was added from the report.
Method: documentation only; no commands were run.
