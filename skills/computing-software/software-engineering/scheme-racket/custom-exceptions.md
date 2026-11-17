---
id: computing-software.software-engineering.scheme-racket.custom-exceptions
name: custom-exceptions
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, custom-exceptions]
level: practitioner
status: docs-checked
description: "Define exception types with struct inheriting exn:fail, raise them, and catch with their predicate."
sources:
  - https://docs.racket-lang.org/guide/control.html
  - https://docs.racket-lang.org/reference/exns.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Custom exception structs
**Goal:** typed errors.
```racket
(struct exn:my exn:fail (code))
(raise (exn:my "boom" (current-continuation-marks) 42))
(with-handlers ([exn:my? exn:my-code]) (raise (exn:my "x" (current-continuation-marks) 7)))
```
- Constructor needs `message` and `marks` first, then your fields.
- `raise-user-error` is for errors intended for end users; the default error display handler shows no stack trace for `exn:fail:user`.
## Self-check
The handler returns `7`.

## Checked

Date: 2026-11-02. Confirmed on Racket Reference Exceptions (`exn` has `message` and `continuation-marks` fields, `exn:fail` is a substructure of `exn`; `raise-user-error` and `exn:fail:user`). Removed: nothing.

Method: documentation only; no commands were run.
