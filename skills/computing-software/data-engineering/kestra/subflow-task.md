---
id: computing-software.data-engineering.kestra.subflow-task
name: subflow-task
category: computing-software
field: data-engineering
product: kestra
tags: [subflow, wait, transmitfailed, flow-outputs, kill-cascade]
level: practitioner
status: docs-checked
description: "Call one Kestra flow from another with the Subflow task: inputs, wait, transmitFailed, reading child outputs, and kill and retry caveats."
sources:
  - https://kestra.io/docs/workflow-components/subflows
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Task `io.kestra.plugin.core.flow.Subflow` properties: `flowId`, `namespace`, `inputs`, `labels`, `inheritLabels` (default `false`), `revision` (default latest), `scheduleDate`, `wait` (default `true`), `transmitFailed` (default `true`, requires `wait: true`). `outputs` is deprecated; use flow outputs.

```yaml
tasks:
  - id: subflow_call
    type: io.kestra.plugin.core.flow.Subflow
    namespace: company.team
    flowId: critical_service
    wait: true
    transmitFailed: true

  - id: log_subflow_output
    type: io.kestra.plugin.core.log.Log
    message: "{{ outputs.subflow_call.outputs.some_output }}"
```

With `wait: false` the parent continues. With `transmitFailed: false` a subflow failure does not fail the parent.

Caveats:

- Recursion is not supported; use Loop or LoopUntil.
- "Kill current and subflows" kills parent and subflow; "Kill current only" lets the subflow finish first.
- The single-execution kill API kills subflows by default; add `?isOnKillCascade=false` to avoid it. Bulk kill endpoints never kill subflows.
- Killing the subflow directly: with `transmitFailed: true` the parent ends `FAILED`, or `WARNING` if also `allowFailure: true`.
- A retry on the Subflow task does not restart a killed subflow execution.

## Checked

2026-11-04. Confirmed against "Call Flows from Other Flows and Build Reusable Components" (workflow-components/subflows): property table and defaults, wait and transmitFailed, recursion not supported with LoopUntil suggestion, kill options and API behaviour including isOnKillCascade and bulk endpoints, killed-subflow outcome table, retry note, outputs access form. No claims removed.
Method: documentation only; no commands were run.
