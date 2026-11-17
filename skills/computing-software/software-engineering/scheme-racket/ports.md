---
id: computing-software.software-engineering.scheme-racket.ports
name: ports
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, ports, racket-io]
level: intro
status: docs-checked
description: "Read and write via ports: current-input-port, current-output-port, display, write, newline, read-line, read, peek-char."
sources:
  - https://docs.racket-lang.org/reference/ports.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Ports and the current ports
**Goal:** I/O basics.
```racket
(displayln "hi")
(write "x")          ; "x" with quotes
(define l (read-line (current-input-port)))   ; eof when closed
(eof-object? l)
```
- `display` for humans, `write` for readable re-parse, `print` for REPL style.
- `read-line` returns `eof`, check with `eof-object?`.
## Self-check
`(write "a")` prints with quotes; `(display "a")` without.

## Checked

2026-11-02. Confirmed against the Racket Reference, Guide, Foreign Interface, raco and pkg manuals at docs.racket-lang.org (pages named in sources): the functions, keywords, flags and behaviours stated above. Removed or corrected claims the pages did not support (see the version history). Example outputs are illustrative.

Method: documentation only; no commands were run.
