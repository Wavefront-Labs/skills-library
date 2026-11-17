---
id: computing-software.devops-ci-cd.awx-operator.awx-operator-container-probes-liveness-readiness
name: awx-operator-container-probes-liveness-readiness
category: computing-software
field: devops-ci-cd
product: awx-operator
tags: [awx-operator, liveness-probe, readiness-probe, web, task, supervisor, awx-manage]
level: practitioner
status: docs-checked
description: "Enable the disabled-by-default liveness and readiness probes for AWX web and task containers by setting the period parameters."
sources: ["https://github.com/ansible/awx-operator/blob/devel/docs/user-guide/advanced-configuration/container-probes.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Awx operator container probes liveness readiness

All probes are disabled by default for now; enable them by setting the `*_period` parameters:

```yaml
spec:
  web_liveness_period: 15
  web_readiness_period: 15
  task_liveness_period: 15
  task_readiness_period: 15
```

A period of 0 disables the probe.

- Liveness (web and task): queries the status of the container's supervisor daemon and fails if any service is in a state other than "RUNNING".
- Web readiness: an HTTP check against the status endpoint to confirm the system is still able to respond to web requests.
- Task readiness: a command probe using the builtin check command of the `awx-manage` utility.

Each of `web_liveness_`, `web_readiness_`, `task_liveness_` and `task_readiness_` has four parameters, with defaults:
- `period`: seconds between probe checks (0, which disables the probe).
- `initial_delay`: initial delay before starting probes, in seconds (5).
- `failure_threshold`: consecutive failure events that identify failure of the container (3).
- `timeout`: seconds to wait for a probe response from the container (1).

For example `web_readiness_failure_threshold` and `task_liveness_initial_delay`.

## Checked

2026-11-04. Confirmed against the AWX Operator "Container Probes" page: all 16 parameter names, descriptions and defaults, the three probe descriptions, and the period example. Removed the claim that probes are only created once the period is non-zero and the "16 settings" pattern line.
Method: documentation only; no commands were run.
