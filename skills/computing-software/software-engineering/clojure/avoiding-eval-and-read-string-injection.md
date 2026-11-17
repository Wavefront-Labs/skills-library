---
id: computing-software.software-engineering.clojure.avoiding-eval-and-read-string-injection
name: avoiding-eval-and-read-string-injection
category: computing-software
field: software-engineering
product: clojure
tags: [clojure, security, eval, read-string, read-eval, injection, edn, load-string, untrusted-input, rce, security-eval-read-injection, clojure-security]
level: advanced
status: gated
description: "Avoid remote code execution from untrusted input: never eval or load-string user data, use clojure.edn/read-string, bind *read-eval* false, and sandbox carefully."
sources: ["https://clojure.org/reference/reader", "https://owasp.org/www-project-top-ten/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Eval and read injection

**Goal:** make sure data never becomes code.

```clojure
(read-string "#=(java.lang.Runtime/exec \"calc\")")   ; DANGEROUS: #= executes when *read-eval* is true
(binding [*read-eval* false] (read-string s))          ; safe for plain data
(clojure.edn/read-string s)                            ; preferred for untrusted data
```
- Never pass user-controlled text to `eval`, `load-string`, `load-file`, `read-string` (default), `resolve` +
  invocation, `(ns-resolve ...)` on arbitrary symbols, or `(requiring-resolve (symbol input))`.
- JVM property `-Dclojure.read.eval=false` (and `unknown`) disables `#=` globally; set it in production
  (see `*read-eval*` docs).
- Deserialising Java objects (`ObjectInputStream`) from untrusted input is a separate RCE vector; avoid or filter.
- Limit EDN input size and depth at the transport layer to prevent resource exhaustion.
- Tagged-literal readers you add (`:readers`) must be pure and safe; never include a reader that evaluates.
- Exposed REPLs (nREPL, socket REPL) are RCE by design: bind to localhost, firewall, authenticate via tunnel.
- Plugin systems: if you must load user code, run it in a separate process or container with limited privileges;
  Clojure itself is not a sandbox.

## Failure modes
- `*read-eval*` left true in an HTTP handler that reads request bodies.
- Using `eval` for config templating.

## Self-check
Confirm that `(clojure.edn/read-string "#=(+ 1 1)")` throws, while core `read-string` with `*read-eval*` true evaluates.

## Checked

- Date: 2026-11-02.
- Source pages listed in `sources` were fetched where possible; reader page read; *read-eval*, #= and clojure.edn specifics are not on the fetched page. Treat the specific names, flags and figures as unconfirmed (gated: unconfirmed, source is paywalled or blocked).

Method: documentation only; no commands were run.
