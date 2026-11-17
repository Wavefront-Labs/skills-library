---
id: computing-software.devops-ci-cd.kustomize.composing-resources-and-patches
name: composing-resources-and-patches
category: computing-software
field: devops-ci-cd
product: kustomize
tags: [resources, patches, compose, replicas, memory]
level: intro
status: docs-checked
description: "Compose a Deployment and Service with resources, then customize with small patch files for replicas and memory limit."
sources:
  - "https://kubernetes.io/docs/tasks/manage-kubernetes-objects/kustomization/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Composition uses the `resources` list to include files:

```yaml
resources:
- deployment.yaml
- service.yaml
```

Customization uses `patches`. Create one small patch per change:

```yaml
# increase_replicas.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-nginx
spec:
  replicas: 3
```

```yaml
# set_memory.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-nginx
spec:
  template:
    spec:
      containers:
      - name: my-nginx
        resources:
          limits:
            memory: 512Mi
```

```yaml
resources:
- deployment.yaml
patches:
- path: increase_replicas.yaml
- path: set_memory.yaml
```

The target resource is matched using the `group`, `version`, `kind` and `name` from the patch file. The result has `replicas: 3` and a memory limit of `512Mi` on container `my-nginx`.

When strategic merge cannot reach a field, use JSON6902 with a required `target`:

```yaml
patches:
- target:
    group: apps
    version: v1
    kind: Deployment
    name: my-nginx
  path: patch.yaml
```

with `patch.yaml` containing `- op: replace`, `path: /spec/replicas`, `value: 3`.

Not all resources or fields support strategic merge patches, which is why JSON6902 exists.

## Checked

2026-11-03. Confirmed against: the Kubernetes kustomization task page and the patches reference page.
Removed or reworded: nothing needed removing; all claims matched the pages.

Method: documentation only; no commands were run.
