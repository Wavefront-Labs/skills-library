---
id: computing-software.data-engineering.kestra.task-timeout
name: task-timeout
category: computing-software
field: data-engineering
product: kestra
tags: [timeout, iso-8601, max-duration, runnable-tasks]
level: intro
status: docs-checked
description: "Limit Kestra runnable task duration with timeout in ISO 8601 format, and use an SLA MAX_DURATION when you need a flow-wide limit."
sources:
  - https://kestra.io/docs/workflow-components/timeout
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`timeout` sets the maximum duration of a runnable task. If exceeded, Kestra stops the task and marks it failed. This guards against hung processes and runaway cost on long cloud jobs.

Format is ISO 8601 duration; week, month and year designators are not supported.

- `PT0.250S`: 250 milliseconds
- `PT2S`: 2 seconds
- `PT1M`: 1 minute
- `PT3.5H`: 3 hours 30 minutes
- `P6DT4H`: 6 days 4 hours

```yaml
tasks:
  - id: costly_query
    type: io.kestra.plugin.scripts.shell.Commands
    taskRunner:
      type: io.kestra.plugin.core.runner.Process
    commands:
      - sleep 10
    timeout: PT5S
```

This task sleeps 10 seconds against a 5 second timeout, so it fails.

There is no flow-level timeout. To cancel an execution that runs too long, use an SLA of type `MAX_DURATION`.

## Checked

2026-11-04. Confirmed against the Kestra timeout page: timeout as maximum duration of a runnable task, failure on exceeding, ISO 8601 with week, month and year designators unsupported, the five duration examples, the sleep 10 against PT5S example, no flow-level timeout and MAX_DURATION SLA as the alternative. Nothing removed.

Method: documentation only; no commands were run.
