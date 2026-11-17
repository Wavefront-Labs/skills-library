---
id: computing-software.data-engineering.kestra.flow-sla
name: flow-sla
category: computing-software
field: data-engineering
product: kestra
tags: [sla, max-duration, execution-assertion, alerting, labels]
level: practitioner
status: docs-checked
description: "Define Kestra SLAs with MAX_DURATION and EXECUTION_ASSERTION, choose CANCEL, FAIL or NONE on breach, and alert through the sla: miss label."
sources:
  - https://kestra.io/docs/workflow-components/sla
  - https://kestra.io/docs/workflow-components/timeout
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`sla` is a root-level flow property listing checks. Each has `id`, `type`, `behavior`, optional `labels`.

Types:

- `MAX_DURATION`: needs `duration` (ISO 8601). The clock starts at execution creation, so `QUEUED` time counts.
- `EXECUTION_ASSERTION`: needs `assert`, a Pebble expression; false means breach.

Behaviors: `CANCEL`, `FAIL`, `NONE` (log only).

```yaml
sla:
  - id: maxDuration
    type: MAX_DURATION
    duration: PT8H
    behavior: CANCEL
    labels:
      sla: miss
      reason: durationExceeded

  - id: assert_output
    type: EXECUTION_ASSERTION
    assert: "{{ outputs.mytask.values.result == 'expected output' }}"
    behavior: FAIL
```

Alert on breaches with a Flow trigger that listens for the label:

```yaml
triggers:
  - id: alert_on_failure
    type: io.kestra.plugin.core.trigger.Flow
    dependsOn:
      - labels:
          sla: miss
        states: [FAILED, WARNING, CANCELLED]
```

SLA `MAX_DURATION` is the way to cap total execution time, since there is no flow-level timeout.

## Checked

2026-11-04. Confirmed against the Kestra SLA page: sla root property, MAX_DURATION counting from creation including QUEUED time, EXECUTION_ASSERTION, CANCEL, FAIL and NONE behaviors, labels, Flow trigger alert on sla: miss. The no-flow-level-timeout statement is confirmed on the Kestra timeout page, now added to sources. Nothing removed.

Method: documentation only; no commands were run.
