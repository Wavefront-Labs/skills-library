---
id: computing-software.devops-ci-cd.argo-workflows.high-availability
name: high-availability
category: computing-software
field: devops-ci-cd
product: argo-workflows
tags: [high-availability, leader-election, recreate-strategy, pod-disruption-budget, priority-class]
level: advanced
status: docs-checked
description: "Choose between a single workflow controller replica with leader election disabled and multiple replicas, plus Argo Server replica guidance."
sources: ["https://argo-workflows.readthedocs.io/en/latest/high-availability/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# High availability for controller and server
Neither the controller nor the Argo Server has resource requests or limits by default; set requests. For several replicas of a deployment, spread pods over availability zones (at least across nodes) and add a PodDisruptionBudget.

Controller, single replica (recommended for most cases, because re-provisioning a pod is often faster than winning a leader election under load, and standby pods waste resources): set the environment variable `LEADER_ELECTION_DISABLE=true` and use the installation manifests' `workflow-controller` PriorityClass so it schedules first. Disabling election avoids needless Kubernetes API traffic. Then the Deployment must not surge: the default RollingUpdate `maxSurge: 25%` rounds to 1, so the new pod becomes Ready before the old one stops and both reconcile the same Workflows, duplicating pods and clobbering status. Set:

```yaml
spec:
  strategy:
    type: Recreate
```
Cost is a few seconds of downtime; running Workflows continue.

Multiple replicas: keep leader election on (omit the variable or `false`). One replica is active, the others standby; RollingUpdate is safe. Election needs frequent API calls, and at scale it may take longer than 10 seconds (`LEADER_ELECTION_RENEW_DEADLINE`), disrupting the controller.

Argo Server: run at least two, typically three replicas to avoid dropped API and webhook requests; it is horizontally scalable and can be load balanced, but its minimum memory at scale is large and not load dependent.

## Checked
2026-11-03. Confirmed against the Argo Workflows High-Availability page: resource requests, spreading and PodDisruptionBudget, single replica guidance with `LEADER_ELECTION_DISABLE` and the PriorityClass, the Recreate strategy reasoning, multiple replica behaviour and the 10 second `LEADER_ELECTION_RENEW_DEADLINE`, and Argo Server replicas. Nothing removed.
Method: documentation only; no commands were run.
