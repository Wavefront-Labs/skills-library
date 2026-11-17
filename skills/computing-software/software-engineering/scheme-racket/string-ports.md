---
id: computing-software.software-engineering.scheme-racket.string-ports
name: string-ports
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, string-ports]
level: practitioner
status: docs-checked
description: "Capture or feed text using open-output-string, get-output-string, open-input-string and with-output-to-string."
sources:
  - https://docs.racket-lang.org/reference/port-lib.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# String and byte ports
**Goal:** test I/O without files.
```racket
(require racket/port)
(with-output-to-string (lambda () (display "hi")))   ; "hi"
(define o (open-output-string)) (write 'a o) (get-output-string o)
(port->lines (open-input-string "a\nb"))
```
- `port->string`, `port->lines` are in `racket/port`.
## Self-check
`(read (open-input-string "(1 2)"))` returns `'(1 2)`.

## Checked

2026-11-02. Confirmed against the Racket Reference, Guide, Foreign Interface, raco and pkg manuals at docs.racket-lang.org (pages named in sources): the functions, keywords, flags and behaviours stated above. Removed or corrected claims the pages did not support (see the version history). Example outputs are illustrative.

Method: documentation only; no commands were run.
