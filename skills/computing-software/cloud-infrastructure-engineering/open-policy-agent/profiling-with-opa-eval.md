---
id: computing-software.cloud-infrastructure-engineering.open-policy-agent.profiling-with-opa-eval
name: profiling-with-opa-eval
category: computing-software
field: cloud-infrastructure-engineering
product: open-policy-agent
tags: [profiling, opa-eval, profile-sort, num-gen-expr, performance]
level: advanced
status: docs-checked
description: "Profile slow Rego with opa eval --profile, --profile-sort and --profile-limit, read TIME, NUM EVAL, NUM REDO and NUM GEN EXPR columns, and early-exit conditions."
sources:
  - https://www.openpolicyagent.org/docs/policy-performance
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: find which expressions make evaluation slow.

Options on `opa eval`:
- `--profile` enables expression profiling and prints results
- `--profile-sort` sets the sort criteria (implies `--profile`)
- `--profile-limit` caps how many rows are shown (implies `--profile`)
- `--count` repeats evaluation to capture metrics; with `--format=pretty` it reports min, max, mean and the 90th and 99th percentile


Reading the table (columns TIME, NUM EVAL, NUM REDO, NUM GEN EXPR, LOCATION): each row is a source location. NUM GEN EXPR is the number of expressions the compiler generated for that line. For `x = a + (b * c)` the compiler rewrites it into `mul(...)`, `plus(...)` and an assignment, so the line shows 3 generated expressions and 3 evaluations even though it is one statement. Use that column to explain surprising EVAL and REDO counts.

Early exit: OPA normally iterates every binding, but may stop once more iterations cannot change the result. This applies to sets of complete-document rules that only have one, ground value, and to function rules with one ground value, most commonly a group of `allow` rules (`allow if {...}` is shorthand for `allow := true if {...}`). Writing rules with a variable in the value defeats early exit.

Check: profile with `--profile-sort num_eval` before and after a change and confirm the hot line's NUM EVAL falls.

## Checked

2026-11-04. Confirmed against the OPA docs Policy Performance page, sections Profiling and Early Exit in Rule Evaluation: the --profile, --profile-sort, --profile-limit and --count options (pretty output reports min, max, mean and the 90th and 99th percentile), the sort criteria, the NUM GEN EXPR explanation with the x = a + (b * c) example (3 generated expressions, EVAL and REDO of 3), and early exit for complete-document and function rules with one ground value (typically allow rules), where a variable in the value defeats it. Reworded one phrase; nothing else removed.

Method: documentation only; no commands were run.
