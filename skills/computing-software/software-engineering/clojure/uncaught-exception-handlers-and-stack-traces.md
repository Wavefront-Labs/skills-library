---
id: computing-software.software-engineering.clojure.uncaught-exception-handlers-and-stack-traces
name: uncaught-exception-handlers-and-stack-traces
category: computing-software
field: software-engineering
product: clojure
tags: [clojure, stack-trace, uncaught-exception, set-default-uncaught-exception-handler, pst, clojure-stacktrace, repl-error, tap, uncaught-handlers-stacktraces]
level: practitioner
status: draft
description: "Read Clojure stack traces, use pst and *e at the REPL, install a default uncaught exception handler for threads and agents, and shorten noisy traces."
sources: ["https://clojure.org/reference/repl_and_main", "https://clojure.github.io/clojure/clojure.repl-api.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Uncaught exceptions and stack traces

**Goal:** diagnose crashes quickly and avoid silent thread death.

```clojure
(pst)                    ; print stack trace of *e (clojure.repl)
(pst e 12)               ; limit frames
(ex-data *e)  (ex-cause *e)
(Thread/setDefaultUncaughtExceptionHandler
  (reify Thread$UncaughtExceptionHandler
    (uncaughtException [_ thread ex] (log/error ex "uncaught on" (.getName thread)))))
(clojure.main/repl-caught *e)                        ; formatted
```
- Since Clojure 1.10 compile errors print a concise "Syntax error compiling at (file:line:col)" with the cause
  and a data map; the full trace is written to a temp file (path printed) when `clojure.main` reports.
- Clojure frames look like `my.app.core$fn__1234.invoke(core.clj:10)`; read the namespace and file:line, ignore
  `clojure.lang.*` internal frames.
- Exceptions in `future`, `send` and `core.async` go-blocks do not reach the main thread: they appear at
  `deref`, `agent-error` or via the default handler.
- Set `-Dclojure.main.report=stderr` (1.10+) to print full traces to stderr instead of a temp file.
- In production, install the default handler early in `-main` and in thread pools you create.

## Failure modes
- A thread dies silently because nothing logs it.
- Infinite error loops from handlers that throw.

## Self-check
`(def f (future (/ 1 0)))` prints nothing until `@f` throws; a plain `(.start (Thread. #(/ 1 0)))` reaches your handler.
