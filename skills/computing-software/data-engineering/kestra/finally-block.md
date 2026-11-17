---
id: computing-software.data-engineering.kestra.finally-block
name: finally-block
category: computing-software
field: data-engineering
product: kestra
tags: [finally, cleanup, teardown, errors, execution-state]
level: practitioner
status: docs-checked
description: "Use the Kestra finally block for teardown that always runs, and how it differs from errors and afterExecution."
sources:
  - https://kestra.io/docs/workflow-components/finally
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`finally` tasks always run at the end of a flow, whether the execution succeeds, fails or is killed. Use it for teardown such as stopping a container the flow started.

```yaml
tasks:
  - id: fail
    type: io.kestra.plugin.core.execution.Fail
    errorMessage: Test downstream tasks

errors:
  - id: send_alert
    type: io.kestra.plugin.core.log.Log
    message: alert on failure

finally:
  - id: cleanup_task
    type: io.kestra.plugin.core.log.Log
    message: cleaning up resources
```

Comparison:

- `errors`: runs only when a task or the flow fails.
- `finally`: always runs, while the execution is still `RUNNING`.
- `afterExecution`: runs after the execution settles and can read the final state.

Because `finally` runs while the execution is still `RUNNING`, it cannot act on the final status. Use `afterExecution` for that.

## Checked

2026-11-04. Confirmed against the Kestra finally page: finally always runs including on kill, runs while the execution is still RUNNING, errors runs only on failure, afterExecution for terminal state, container teardown example. Nothing removed.

Method: documentation only; no commands were run.
