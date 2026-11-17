---
id: computing-software.devops-ci-cd.awx-operator.awx-operator-container-resource-requirements-and-quotas
name: awx-operator-container-resource-requirements-and-quotas
category: computing-software
field: devops-ci-cd
product: awx-operator
tags: [awx-operator, resource-requirements, requests, limits, resourcequota, rsyslog, redis]
level: practitioner
status: docs-checked
description: "Set requests and limits for the AWX web, task, EE, redis, rsyslog, postgres and init containers, which a ResourceQuota requires."
sources: ["https://github.com/ansible/awx-operator/blob/devel/docs/user-guide/advanced-configuration/containers-resource-requirements.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Awx operator container resource requirements and quotas

Both the lower end (requests) and the upper end (limits) of each container's resources are configurable on the AWX spec. Defaults are requests only:
- `web_resource_requirements`, `task_resource_requirements`, `redis_resource_requirements`, `rsyslog_resource_requirements`, `init_container_resource_requirements`: cpu 100m, memory 128Mi.
- `ee_resource_requirements` (EE control plane container): cpu 50m, memory 64Mi.
- `postgres_resource_requirements` (container and initContainer): cpu 10m, memory 64Mi.

```yaml
spec:
  task_resource_requirements:
    requests:
      cpu: 100m
      memory: 128Mi
      ephemeral-storage: 100M
    limits:
      cpu: 2000m
      memory: 4Gi
      ephemeral-storage: 500M
  web_resource_requirements:
    requests: {cpu: 100m, memory: 128Mi}
    limits: {cpu: 1000m, memory: 4Gi}
  rsyslog_resource_requirements:
    limits: {cpu: 1000m, memory: 2Gi}
```

If the cluster has a ResourceQuota, you need to configure resource limits for all pods deployed there; for AWX pods this is done on the AWX spec as above. The repo has an example, `awx_v1beta1_awx_resource_limits.yaml`.

## Checked

2026-11-04. Confirmed against the AWX Operator "Containers Resource Requirements" page: the seven setting names, their defaults, the example values and the ResourceQuota note. Removed the closing paragraph (ephemeral-storage commentary, restated mappings).
Method: documentation only; no commands were run.
