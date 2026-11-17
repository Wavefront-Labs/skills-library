---
id: computing-software.software-engineering.scheme-racket.racket-base
name: racket-base
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, racket-base]
level: intro
status: docs-checked
description: "Choose between #lang racket and racket/base: which libraries (racket/list, racket/string, racket/match) racket/base omits and what to require."
sources:
  - https://docs.racket-lang.org/reference/pairs.html
  - https://docs.racket-lang.org/reference/strings.html
  - https://docs.racket-lang.org/reference/match.html
  - https://docs.racket-lang.org/guide/macros.html
  - https://docs.racket-lang.org/reference/stx-patterns.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# racket vs racket/base
**Goal:** pick the module language deliberately.
- The manual marks `racket/list`, `racket/string` and `racket/match` bindings as provided by that library and by `racket`, but not by `racket/base`.
- Under `racket/base`, add what you use, for example `(require racket/list racket/string racket/match)`.
- `first` and `take` are in `racket/list`; `string-split`, `string-join`, `string-replace` and `string-trim` are in `racket/string`; `match` is in `racket/match`.
- An unbound `first`, `string-join` or `match` under `racket/base` therefore means a missing `require`, not a typo.
- Most syntactic forms of `racket/base` and `racket` are macros that expand into a small set of core constructs.
- To write macro transformers under `racket/base`, the manual's `syntax-case` example first requires `(for-syntax racket/base)`.
## Self-check
Change a file's `#lang racket` to `racket/base`, note the unbound identifiers, and fix them with the requires above.
## Checked
2026-11-08. Confirmed on the Reference pairs, strings and match pages: the "provided by ... but not racket/base" statements and function membership; on the Guide macros page: forms being macros over core constructs; on the Reference syntax-case page: the `(require (for-syntax racket/base))` example. Removed: the claims that `racket` re-exports format, contracts and class libraries, that `racket/base` loads faster or is preferred for large apps, that the `for` family lives in `racket/base`, and the `time racket file.rkt` comparison.
Method: documentation only; no commands were run.
