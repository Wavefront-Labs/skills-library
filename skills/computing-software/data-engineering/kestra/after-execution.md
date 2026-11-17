---
id: computing-software.data-engineering.kestra.after-execution
name: after-execution
category: computing-software
field: data-engineering
product: kestra
tags: [afterexecution, runif, notifications, final-state, execution-state]
level: practitioner
status: docs-checked
description: "Run Kestra tasks after an execution reaches a terminal state with afterExecution, branch on the final state with runIf, and know its limits."
sources:
  - https://kestra.io/docs/workflow-components/afterexecution
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`afterExecution` tasks run once the flow reaches a terminal state, so they see the settled state (SUCCESS, FAILED, WARNING). Flow level only.

```yaml
afterExecution:
  - id: onSuccess
    runIf: "{{ execution.state == 'SUCCESS' }}"
    type: io.kestra.plugin.slack.notifications.SlackIncomingWebhook
    url: https://hooks.slack.com/services/xxxxx
    messageText: "{{ flow.namespace }}.{{ flow.id }} finished successfully!"

  - id: onFailure
    runIf: "{{ execution.state == 'FAILED' }}"
    type: io.kestra.plugin.slack.notifications.SlackIncomingWebhook
    url: https://hooks.slack.com/services/xxxxx
    messageText: "{{ flow.namespace }}.{{ flow.id }} failed"
```

Caveats:

- An error inside `afterExecution` does not change the final state. A failing task there will not turn SUCCESS into FAILED and will not trigger flows listening for FAILED.
- To force a state change, put the work in a Sequential task with its own `errors` block.

Compared with `errors` and `finally`, both of which run while the execution still shows RUNNING.

## Checked

2026-11-04. Confirmed against the Kestra afterExecution page: runs after a terminal state, runIf state branching, flow-level only, errors inside it do not change the final state, Sequential with its own errors block, finally and errors show RUNNING. Nothing removed.

Method: documentation only; no commands were run.
