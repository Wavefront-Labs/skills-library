---
id: computing-software.devops-ci-cd.argo-events.argo-events-sensor-expr-filter-govaluate
name: argo-events-sensor-expr-filter-govaluate
category: computing-software
field: devops-ci-cd
product: argo-events
tags: [argo-events, expr-filter, govaluate, exprs, fields, exprlogicaloperator]
level: practitioner
status: docs-checked
description: "Evaluate boolean expressions over named event fields in a Sensor with the govaluate-based expr filter."
sources: ["https://github.com/argoproj/argo-events/blob/master/docs/sensors/filters/expr.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Argo events sensor expr filter govaluate

Expr filters evaluate an expression against values pulled from the event `data` payload.

```yaml
filters:
  exprLogicalOperator: "or"
  exprs:
    - expr: a == "b" || c != 10
      fields:
        - name: a
          path: a
        - name: c
          path: c
    - expr: e == false
      fields:
        - name: e
          path: d.e
```

`fields` maps an arbitrary parameter `name` (used in `expr`) to a `path` in the data payload. Expressions are evaluated with the govaluate library: arithmetic (`-`, `*`, `/`, `**`, `%`), negation, inversion (`!`), bitwise not (`~`), logical `&&` and `||`, ternary `?:`, comparators, comma-separated arrays and custom functions. Regex-style match with `=~`, e.g. `action =~ "start" || (started == true && instances == 2)`.

Filters evaluate in declaration order and `exprLogicalOperator` (lower case `and` default or `or`) combines them. Errors, such as a path not found, count as false.

The page's walkthrough applies `examples/sensors/filter-with-expressions.yaml` to the webhook example. Posting `{ "a": "b", "c": 11, "d": { "e": true } }` makes the sensor log the event as invalid because `e == false` is expected; posting the same with `"e": false` produces a workflow named `expr-workflow-...`. That walkthrough's manifest is not reproduced on the page, so do not assume it uses the `or` operator shown above.

## Checked

2026-11-04. Confirmed against the Expr filter page: the fields layout, declaration-order evaluation, `exprLogicalOperator` values (lower case, empty means `and`), errors counting as false, `fields` name and path, govaluate operators and the `=~` example, and the practical example commands and outcomes. Clarified that the walkthrough's operator setting is not shown on the page.
Method: documentation only; no commands were run.
