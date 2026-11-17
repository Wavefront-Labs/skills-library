---
id: computing-software.data-engineering.kestra.flow-trigger-dependson
name: flow-trigger-dependson
category: computing-software
field: data-engineering
product: kestra
tags: [flow-trigger, dependson, windows, satisfaction-mode, upstream-flows]
level: advanced
status: docs-checked
description: "Chain Kestra flows with the Flow trigger: dependsOn entries, ALL/ANY/AT_LEAST modes, when conditions, time windows, and reading upstream outputs."
sources:
  - https://kestra.io/docs/workflow-components/triggers/flow-trigger
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Type `io.kestra.plugin.core.trigger.Flow` runs a flow after upstream flows complete.

```yaml
triggers:
  - id: after_extract
    type: io.kestra.plugin.core.trigger.Flow
    inputs:
      date: "{{ trigger.outputs.date }}"
    dependsOn:
      - flowId: extract
        namespace: company.team
        states: [SUCCESS]
```

Each `dependsOn` entry: `flowId` (omit to match any), `namespace` (exact match), `states` (default all terminal states and `PAUSED`), `labels`, `when`.

Satisfaction mode: `ALL` (default), `ANY`, or `AT_LEAST` with `minSatisfied` (integer >= 1).

Conditions: a top-level `when` runs before `dependsOn`. Entry `when` may use `flow.namespace`, `flow.id`, `labels`, `execution.outputs`, `execution.state`, `execution.attemptNumber`. For prefix matching omit `namespace` and use `{{ flow.namespace | startsWith('company') }}`.

`window` options: `deadline`, `from`/`to`, `every`/`offset`, `lookback`, `timezone` (defaults to the server timezone).

Caveats:

- With several upstream flows, only the last-completed flow's outputs are in `trigger.outputs`.
- After firing, every dependency must be satisfied again.
- A `when` that fails to render does not fire; a failing `inputs` expression creates a `FAILED` execution.
- `preconditions` and `conditions` were removed in 2.0; migrate to `dependsOn`.

## Checked

2026-11-04. Confirmed against the Kestra Flow trigger page: dependsOn entry properties and defaults, ALL, ANY and AT_LEAST with minSatisfied, top-level when evaluated before dependsOn, entry when variables, window options and server timezone default, trigger.outputs holding only the last upstream execution, reset after firing, failed rendering behaviour, removal of preconditions and conditions in 2.0. Nothing removed.

Method: documentation only; no commands were run.
