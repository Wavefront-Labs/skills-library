---
id: computing-software.devops-ci-cd.kustomize.patches-strategic-merge-deprecated
name: patches-strategic-merge-deprecated
category: computing-software
field: devops-ci-cd
product: kustomize
tags: [patchesstrategicmerge, deprecated, delete, patches]
level: intro
status: docs-checked
description: "patchesStrategicMerge is deprecated since v5.0.0; migrate to patches, and keep delete directives in a single patch per object."
sources:
  - "https://kubectl.docs.kubernetes.io/references/kustomize/kustomization/patchesstrategicmerge/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`patchesStrategicMerge` was deprecated in v5.0.0. It stays in the v1beta1 API forever but will not be in a future v1. Move entries to `patches`, which supports the same patches with slightly different syntax. `kustomize edit fix` converts them automatically.

Each entry is a relative file path or inline content resolving to a partial or complete resource definition:

```yaml
patchesStrategicMerge:
- service_port_8888.yaml
- deployment_increase_replicas.yaml
- |-
  apiVersion: apps/v1
  kind: Deployment
  metadata:
    name: nginx
  spec:
    template:
      spec:
        containers:
        - name: nginx
          image: nignx:latest
```

Rules from the page:

- Names in the patch must match names already loaded via `resources`.
- Small patches that do one thing (a memory limit, an env var) are best.
- Kustomize does not support more than one patch for the same object that contains a delete directive. To remove several fields or list elements, write a single patch that performs all the deletions.
- A patch can refer to a resource by any previous name or kind.

Converted form:

```yaml
patches:
- path: service_port_8888.yaml
- path: deployment_increase_replicas.yaml
```

## Checked

2026-11-03. Confirmed against: the patchesStrategicMerge and patches reference pages.
Removed or reworded: nothing needed removing; all claims matched the pages.

Method: documentation only; no commands were run.
