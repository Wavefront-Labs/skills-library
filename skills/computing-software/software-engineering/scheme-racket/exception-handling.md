---
id: computing-software.software-engineering.scheme-racket.exception-handling
name: exception-handling
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, exception-handling]
level: practitioner
status: docs-checked
description: "Raise errors with error and raise and handle them with with-handlers, selecting on predicates such as exn:fail? and exn:fail:contract:divide-by-zero?."
sources:
  - https://docs.racket-lang.org/reference/exns.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# raise, with-handlers and error
**Goal:** catch and report errors.
```racket
(with-handlers ([exn:fail:contract:divide-by-zero? (lambda (e) 'div0)]
                [exn:fail? (lambda (e) (exn-message e))])
  (/ 1 0))
(error 'tag "bad value ~a" 5)   ; message "tag: bad value 5"
(raise 'any-value)   ; any value can be raised
```
- `with-handlers` tries each `pred-expr` in order on the raised value; the first true one has its handler called with the exception, and the handler's result is the value of the whole `with-handlers`. If no predicate matches, the exception is raised again from the `with-handlers` continuation.
- Before a predicate or handler runs, the continuation of the `with-handlers` expression is restored (the handler runs after unwinding), with breaks disabled.
- `exn:fail?` catches all error exceptions; `exn:break` is not an `exn:fail`. The Reference warns against a catch-all predicate such as `(lambda (x) #t)` because `exn:break` typically should not be caught, and against discarding error messages (consider `log-error`).
- `(raise v [barrier?])`: `v` can be anything; `barrier?` defaults to `#t` and protects the handler call with a continuation barrier. Exceptions raised by Racket functions behave as if `barrier?` were `#t`.
- `error` forms: `(error message-sym)` gives `error: <sym>`; `(error message-str v ...)` appends the `v`s after a space each; `(error who-sym format-str v ...)` formats as `"~s: "` followed by `format-str`. The Reference says to prefer `raise-argument-error` or `raise-arguments-error` for conventional messages.
## Self-check
The handler for `exn:fail?` is not reached for the division above: the more specific `exn:fail:contract:divide-by-zero?` clause comes first and returns `'div0`. Swap the clause order and `(exn-message e)` returns the division-by-zero message string instead.

## Checked
2026-11-08. Read: Racket Reference 10.2 Exceptions (reference/exns.html), the 10.2.2 Raising Exceptions section in full (`raise`, `error` and their examples) and the `with-handlers` entry; searched the exception-hierarchy list for `exn:fail:contract:divide-by-zero` and `exn:break`. Fixed the old self-check, which said the `exn:fail?` handler returns the message even though the divide-by-zero clause listed first would win. Removed the vague "`raise` second argument ... rarely changed" and clarified the default and meaning from the page. The `"tag: bad value 5"` comment follows the documented `who-sym format-str` form. Dropped the guide/control index source.
Method: documentation only; no commands were run.
