---
id: computing-software.devops-ci-cd.awx-operator.awx-operator-horizontal-pod-autoscaler-manage-replicas
name: awx-operator-horizontal-pod-autoscaler-manage-replicas
category: computing-software
field: devops-ci-cd
product: awx-operator
tags: [awx-operator, hpa, web-manage-replicas, task-manage-replicas, autoscaling, replicas]
level: advanced
status: docs-checked
description: "Hand the replica count of the AWX web or task deployment to a Horizontal Pod Autoscaler by turning off operator replica management."
sources: ["https://github.com/ansible/awx-operator/blob/devel/docs/user-guide/advanced-configuration/horizontal-pod-autoscaler.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Awx operator horizontal pod autoscaler manage replicas

An HPA scales deployment replicas on metrics, which conflicts with the operator setting a static replica count. Two switches tell the operator not to manage the `replicas` field of a deployment, even if a replicas count is set in the operator resource:

| Name | Meaning | Default |
| --- | --- | --- |
| `web_manage_replicas` | operator controls the web deployment replicas | true |
| `task_manage_replicas` | operator controls the task deployment replicas | true |

```yaml
spec:
  web_manage_replicas: false
  task_manage_replicas: false
```

Then create the HPA objects yourself, following the Kubernetes documentation. The AWX docs say optimal HPA values are cluster specific, so no general guidelines are given.

## Checked

2026-11-04. Confirmed against the AWX Operator "Horizontal Pod Autoscaler (HPA)" page: both setting names, descriptions, defaults (true), the conflict statement and the no-guidelines note. Removed the closing paragraph (independence of the switches and the "why these flags exist" claim) and "targeting the AWX web or task Deployment", none of which the page states.
Method: documentation only; no commands were run.
