---
id: computing-software.software-engineering.scheme-racket.command-line-parsing
name: command-line-parsing
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, command-line-parsing]
level: practitioner
status: docs-checked
description: "Parse flags and positionals with the command-line form from racket/cmdline, including #:once-each, #:args, and --help generation."
sources:
  - https://docs.racket-lang.org/reference/Command-Line_Parsing.html
  - https://docs.racket-lang.org/guide/scripts.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# command-line flags
**Goal:** script options.
```racket
#lang racket/base
(require racket/cmdline)   ; command-line is not in racket/base
(define verbose? (make-parameter #f))
(command-line #:program "tool"
  #:once-each [("-v" "--verbose") "Verbose" (verbose? #t)]
  #:args (file) (printf "~a ~a\n" file (verbose?)))
```
- `command-line` comes from `racket/cmdline` (also provided by `racket`), not `racket/base`.
- Defaults: `#:argv` is `(current-command-line-arguments)`; `#:program` is `(find-system-path 'run-file)` and is used when reporting errors.
- Clause tags: `#:multi` (any number of times), `#:once-each` (each flag at most once, otherwise `exn:fail`), `#:once-any` (mutually exclusive), `#:final`.
- A flag spec is `[flags help-string body ...]` where `flags` is a string or a list of equivalent strings such as `("-v" "--verbose")`; ids listed after the flags receive its arguments as strings.
- `#:args` binds leftover non-flag arguments like a `lambda` formals list (a single id collects them into a list); a wrong count raises `exn:fail`.
- `-h` and `--help` are predefined and cannot be changed; they print generated help. `--` ends the flags.
- `#:usage-help`, `#:help-labels` and `#:ps` add text lines to the usage output.
## Self-check
Run the script with `--help` and read the generated usage, which lists `-v`/`--verbose` and the `file` argument.

## Checked
2026-11-08. Read in full: Racket Reference 15.9 Command-Line Parsing (reference/Command-Line_Parsing.html) and Racket Guide 21.2 Scripts (guide/scripts.html). The old source was the Filesystem page, which does not document `command-line`. Added the `racket/cmdline` requirement (the page says racket/base does not provide it) and the confirmed defaults and clause semantics. Removed the self-check that predicted `racket tool.rkt -v f.txt` output because the pages do not document how the `racket` launcher splits arguments after a file name; replaced it with the `--help` check the Guide suggests.
Method: documentation only; no commands were run.
