---
id: computing-software.software-engineering.clojure.repl-driven-development-workflow
name: repl-driven-development-workflow
category: computing-software
field: software-engineering
product: clojure
tags: [clojure, repl, repl-driven-development, rich-comment, user-clj, reload, tools-namespace, refresh, start-repl, repl-workflow, clojure-repl]
level: intro
status: docs-checked
description: "Develop interactively: start a REPL, evaluate forms from the editor, keep rich comment blocks, reload namespaces safely and avoid stale state."
sources: ["https://clojure.org/guides/repl/introduction", "https://clojure.org/guides/repl/basic_usage", "https://clojure.org/reference/repl_and_main"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# REPL-driven workflow

**Goal:** make the REPL the primary way to build and verify code.

## Start
```bash
clj                                   # start a REPL with the Clojure CLI
```
## Loop
1. Write a small function in the file.
2. Evaluate that form from the editor (or paste it into the REPL; the basic usage guide suggests a syntax-aware
   editor beside the REPL terminal).
3. Call it with sample data in a `(comment ...)` "rich comment" block at the bottom of the file.
4. Evaluate the test, then commit.
```clojure
(comment
  (def sample {:a 1})
  (my-fn sample))
```
- Load a library with `(require '[my.name.space :as x])`; the REPL can run any Clojure program by loading its sources.
- `user.clj` on the classpath is loaded by the Clojure runtime at startup, before the application's main namespace.
  Use it for development helpers only: the reference says it is not recommended in production, and anything it loads
  adds to startup time.
- REPL vars: `*1`, `*2`, `*3` hold the last three results and `*e` the last exception.
- From `clojure.repl` (`(require '[clojure.repl :refer :all])`): `doc`, `source`, `dir`, `apropos` (searches Var names),
  `find-doc` (searches docstrings) and `pst` (stack trace of `*e` by default).
- Documentation lookup only covers namespaces you have required: `(doc clojure.set/union)` returns nothing until
  `clojure.set` is required.
- The first output line of a `println` is a side effect and `nil` is the REPL printing the result: keep the two apart
  when reading output.
- Do not let the REPL image drift: restart periodically and run the full test suite.

## Failure modes
- Stale definitions (renamed or deleted var still defined in the live image).
- Hidden state in `defonce` or atoms that survives reloads.

## Self-check
Delete a function from the file, reload the ns, and verify whether the old var still exists in the live image.

## Checked
2026-11-08. Confirmed: clojure.org guides repl/introduction and repl/basic_usage (read-eval-print loop, `require` with `:as`/`:refer`, `doc`, `source`, `dir`, `apropos`, `find-doc`, docs only for required libs, println side effect versus result, editor next to REPL); clojure.org reference repl_and_main (`user.clj` loading and its caveats, `*1 *2 *3`, `*e`, `pst`). Removed: Leiningen and `clojure -M:repl` commands, rlwrap, `clojure.tools.namespace.repl/refresh` and `:reload` advice, the `restart!` example and the claim about a `dev/` source path, none of which those pages state.
Method: documentation only; no commands were run.
