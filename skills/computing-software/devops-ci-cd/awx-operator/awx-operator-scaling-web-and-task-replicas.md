---
id: computing-software.devops-ci-cd.awx-operator.awx-operator-scaling-web-and-task-replicas
name: awx-operator-scaling-web-and-task-replicas
category: computing-software
field: devops-ci-cd
product: awx-operator
tags: [awx-operator, replicas, web-replicas, task-replicas, scaling, deployments]
level: practitioner
status: docs-checked
description: "Scale AWX web and task deployments separately with web_replicas and task_replicas or together with replicas."
sources: ["https://github.com/ansible/awx-operator/blob/devel/docs/user-guide/advanced-configuration/scaling-the-web-and-task-pods-independently.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Awx operator scaling web and task replicas

Use `replicas` to scale both the web and task deployments to the same number, or `web_replicas` and `task_replicas` for each deployment. Precedence: if `web_replicas` or `task_replicas` is passed, it overrides the `replicas` value for that deployment.

```yaml
spec:
  replicas: 2        # both deployments
  task_replicas: 4   # task overridden
```

Scheduling constraints can be applied per deployment by prefixing the setting with the deployment name (for example `web_tolerations`, `task_node_selector`), as described in the node assignment page.

The operator works with Kubernetes Horizontal Pod Autoscaling; see the HPA page.

## Checked

2026-11-04. Confirmed against the AWX Operator page "Scaling the Web and Task Pods independently": `replicas`, `web_replicas`, `task_replicas`, the override rule, deployment-name prefixes for constraints, and HPA support. Removed the closing paragraph about `web_manage_replicas`/`task_manage_replicas` overwrite behaviour (not on this page; see the HPA skill) and the claim that HPA conflicts with the operator (only on the HPA page).
Method: documentation only; no commands were run.
