---
id: computing-software.devops-ci-cd.argo-events.argo-events-sensor-filters-overview-and-logical-operator
name: argo-events-sensor-filters-overview-and-logical-operator
category: computing-software
field: devops-ci-cd
product: argo-events
tags: [argo-events, filters, sensor, filterslogicaloperator, dependency, and-or]
level: practitioner
status: docs-checked
description: "Understand the five Sensor filter types, the order they are evaluated in and how filtersLogicalOperator combines them."
sources: ["https://github.com/argoproj/argo-events/blob/master/docs/sensors/filters/intro.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Argo events sensor filters overview and logical operator

Sensor filters apply constraints to events to decide whether they are valid. A valid event proceeds towards the Sensor triggers; an invalid one does nothing.

Argo Events has five filter types: Expr, Data, Script, Context and Time. The page's order note lists expr, data, context, time as the order in which the Sensor evaluates filter types; it does not place Script in that order.

Filter types are combined with a logical operator set on the dependency through `filtersLogicalOperator`:
- `and` (also the default for an empty string): every filter must return true.
- `or`: one true filter is enough.

Values must be lower case. Any filter error counts as false, for example a path that does not exist in the event body.

```yaml
spec:
  dependencies:
    - name: sample-dependency
      eventSourceName: webhook
      eventName: sample-event
      filtersLogicalOperator: "or"
      filters:
        # data, exprs, context, time ...
```

The Expr and Data filter pages describe their own operators, `exprLogicalOperator` and `dataLogicalOperator`, with the same values (`and` default, `or`, lower case). More examples are in `examples/sensors` in the repository.

## Checked

2026-11-04. Confirmed against the Filters Introduction page (five types, the evaluation-order note, `and`/`or`, empty string defaulting to `and`, lower case, errors as false, `filtersLogicalOperator` example) and the Expr and Data filter pages (their own operator fields). Reworded the order sentence to match the page, which does not place Script in the order, and removed the "combine at the top level" advice.
Method: documentation only; no commands were run.
