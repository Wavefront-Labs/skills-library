---
id: computing-software.software-engineering.clojure.try-catch-finally-ex-info-ex-data
name: try-catch-finally-ex-info-ex-data
category: computing-software
field: software-engineering
product: clojure
tags: [clojure, exceptions, try, catch, finally, throw, ex-info, ex-data, ex-message, ex-cause, error-handling, ex-info-try-catch, clojure-errors]
level: practitioner
status: docs-checked
description: "Throw and catch exceptions with try/catch/finally, create data-carrying errors with ex-info, ex-data, ex-message and ex-cause, and chain causes."
sources: ["https://clojure.org/reference/special_forms", "https://clojure.github.io/clojure/clojure.core-api.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# try/catch/finally and ex-info

**Goal:** signal and handle failures with data, not strings.

```clojure
(try
  (risky)
  (catch java.io.IOException e (log/warn e "io") :fallback)
  (catch Exception e (throw (ex-info "wrapped" {:input x} e)))   ; cause is the third arg
  (finally (cleanup)))

(try (throw (ex-info "bad input" {:type ::validation :field :age}))
     (catch clojure.lang.ExceptionInfo e
       (ex-data e)       ;=> {:type ::validation :field :age}
       (ex-message e)    ;=> "bad input"
       (ex-cause e)))
(try ... (catch Throwable t ...))   ; includes Errors like OutOfMemoryError: use sparingly
```
- Clauses are tried in order; the first matching class wins.
- `ex-message` and `ex-cause` are accessors on Throwables; `(ex-info msg map cause)` keeps the chain.
- `finally` result is discarded; do not `return` from it.

## Patterns
- Put machine-readable `:type` keys in ex-data and dispatch on them in the catcher.
- Prefer returning data (`{:ok ...}` / `{:error ...}`) for expected failures and exceptions for the unexpected.
- Use `with-open` rather than `try/finally` for closeable resources.

## Failure modes
- Lazy sequences throwing outside the `try` because they realise later.
- Swallowing exceptions: always log or rethrow.

## Self-check
Throw an `ex-info` inside a `map` consumed outside the `try` and observe where it surfaces.

## Checked
2026-11-02. Confirmed: clojure.org/reference/special_forms (try, catch clauses tried in order, finally) and the clojure.core API: ex-info with cause as third argument, ex-data, ex-message, ex-cause, with-open. Removed: the ClojureScript :default note and the recur/try remark.
Method: documentation only; no commands were run.
