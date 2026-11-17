---
id: computing-software.devops-ci-cd.awx-operator.awx-operator-termination-grace-period-and-running-jobs
name: awx-operator-termination-grace-period-and-running-jobs
category: computing-software
field: devops-ci-cd
product: awx-operator
tags: [awx-operator, termination-grace-period, prestop-hook, rollout, jobs, upgrade]
level: practitioner
status: docs-checked
description: "Stop AWX jobs ending in Error during rollouts by setting termination_grace_period_seconds, which adds a PreStop hook that waits for managed jobs."
sources: ["https://github.com/ansible/awx-operator/blob/devel/docs/user-guide/advanced-configuration/pods-termination-grace-period.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Awx operator termination grace period and running jobs

During deployment restarts or rollouts, jobs managed by old AWX pods can end in `Error` state because there is no mechanism to transfer them to new pods. Set `termination_grace_period_seconds` on the AWX spec (default: not set).

It does two things:
- It sets the Pod spec `terminationGracePeriodSeconds` of the AWX Deployment, the time between the termination signal and the forcible kill.
- It adds a `PreStop` hook script that keeps AWX pods in terminating state until it finishes, up to `terminationGracePeriodSeconds`. The hook waits until the pod has no more managed jobs, then succeeds and hands over to the normal AWX termination process. The grace period covers the total time of the PreStop hook plus the container stopping normally.

```yaml
spec:
  termination_grace_period_seconds: <seconds>
```

Set it to the longest time you accept waiting for affected jobs to finish. Waiting jobs can lengthen pod termination during `kubectl rollout restart`, AWX upgrades by the operator, and Kubernetes API-initiated evictions.

## Checked

2026-11-04. Confirmed against the AWX Operator "Pods termination grace period" page: the field, default, both effects, and the three situations. Replaced the invented 3600 example value with a placeholder.
Method: documentation only; no commands were run.
