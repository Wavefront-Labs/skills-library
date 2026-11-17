---
id: computing-software.cloud-infrastructure-engineering.open-policy-agent.rego-error-tracebacks
name: rego-error-tracebacks
category: computing-software
field: cloud-infrastructure-engineering
product: open-policy-agent
tags: [debugging, traceback, strict-builtin-errors, stack-trace, opa-eval]
level: advanced
status: docs-checked
description: "Get an evaluation stack trace for a failing Rego rule with opa eval --strict-builtin-errors, the REPL traceback command, opa run -s, and rego.StackTraces."
sources:
  - https://www.openpolicyagent.org/docs/debugging
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: see the chain of queries that led to an error, not just the failing line.

```
opa eval --strict-builtin-errors -d policy.rego 'data.ex.p'
```

Output names the error then a `Traceback:` with the innermost query first, each frame quoting the expression with bound values spliced in (so `f(0)` and `0 / 0` rather than `f(x)`).

Why `--strict-builtin-errors`: by default a failing built-in leaves the expression undefined instead of raising, so there is no error to annotate. This includes type errors such as `count` over a number. Conflict errors need no extra flag. `opa test` does not surface built-in errors at all today.

REPL: the `traceback` command toggles the same output, then `strict-builtin-errors`, then run the query.

Tracebacks describe state at the point of failure only, so they stay short, unlike `--explain` on a policy that evaluates many expressions.

Server: `opa run -s` turns tracebacks on. An evaluation error is answered with HTTP 500, and querying with `GET /v1/data/ex/p?strict-builtin-errors` returns `errors[].stack_trace` entries carrying `query_id` plus file, row and column; no policy source is included.

Embedding in Go: tracebacks are off by default; enable with `rego.StackTraces(true)` and read frames from `topdown.Error.StackTrace`.

Check: use a rule dividing by zero inside a nested rule and confirm each calling rule appears as a frame.

## Checked

2026-11-04. Confirmed against the OPA docs Debugging page, section Evaluation Stack Traces: opa eval --strict-builtin-errors with a Traceback (innermost query first), the REPL traceback command, why strict built-in errors are needed (including type errors, conflict errors need no flag, opa test does not surface built-in errors), the comparison with --explain, resolved values in frames (f(0), 0 / 0), rego.StackTraces(true) with topdown.Error.StackTrace, opa run -s turning tracebacks on, and the 500 response with stack_trace entries (query_id, file, row, col, no policy source). The Check line is a suggested exercise. Nothing removed.

Method: documentation only; no commands were run.
