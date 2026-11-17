---
id: computing-software.software-engineering.scheme-racket.continuation-marks
name: continuation-marks
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, continuation-marks]
level: advanced
status: docs-checked
description: "Attach dynamic context with with-continuation-mark and read it with continuation-mark-set->list; used for stack traces and parameters."
sources:
  - https://docs.racket-lang.org/reference/wcm.html
  - https://docs.racket-lang.org/reference/contmarks.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Continuation marks
**Goal:** track dynamic context.
```racket
(with-continuation-mark 'key 'v
  (continuation-mark-set-first #f 'key))   ; 'v
```
- `(with-continuation-mark key-expr val-expr result-expr)` maps the key to the value in the current continuation's initial frame. If that frame already has a mark for the key, the mark is replaced. `result-expr` is in tail position.
- `(continuation-mark-set->list mark-set key-v [prompt-tag])` returns the marks for `key-v`, one per frame that has one; `#f` as `mark-set` means `(current-continuation-marks)`. `continuation-mark-set-first` returns the first such mark, or `none-v` (default `#f`) if there is none.
- `(make-continuation-mark-key [sym])` makes a key that is not `equal?` to any other value.
- When Racket creates an exception record for a primitive exception, it fills the `continuation-marks` field with `(current-continuation-marks)`.
- `continuation-mark-set->context` returns an approximate stack trace list for a mark set.
## Self-check
Nest two marks for the same key in non-tail positions (for example inside an argument of `+`) and call `continuation-mark-set->list`; both values are listed, innermost first.

## Checked
2026-11-08. Read in full: Racket Reference 10.5 Continuation Marks (reference/contmarks.html) and 3.19 with-continuation-mark (reference/wcm.html). Confirmed the form's syntax, the replacement rule within one frame, tail position of the result expression, the mark-list definition, argument defaults, `make-continuation-mark-key`, the exception `continuation-marks` field and `continuation-mark-set->context`. Reworded the old tail-position claim to what wcm.html states; replaced the guide/control index source and reference/continuations.html (not the marks page) with these pages. Dropped the wording that `exn` values store context via the function name alone, in favour of the page's exact statement.
Method: documentation only; no commands were run.
