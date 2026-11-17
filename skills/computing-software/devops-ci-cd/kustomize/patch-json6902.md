---
id: computing-software.devops-ci-cd.kustomize.patch-json6902
name: patch-json6902
category: computing-software
field: devops-ci-cd
product: kustomize
tags: [patches, json6902, rfc6902, target, path]
level: advanced
status: docs-checked
description: "Write JSON6902 patches inline or from files, remember target is mandatory, and escape slashes in label keys as ~1."
sources:
  - https://kubectl.docs.kubernetes.io/references/kustomize/kustomization/patches/
  - https://kubernetes.io/docs/tasks/manage-kubernetes-objects/kustomization/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

JSON6902 patches go in the same `patches` list. The `target` field is always required for them.

```yaml
patches:
  - patch: |-
      - op: add
        path: /metadata/labels/app.kubernetes.io~1version
        value: 1.21.0
    target:
      group: apps
      version: v1
      kind: Deployment
  - patch: |-
      - op: replace
        path: /spec/template/spec/containers/0/image
        value: nginx:1.21.0
    target:
      labelSelector: "app.kubernetes.io/name=nginx"
```

From a file, the content can be written as YAML or JSON and must follow the JSON6902 standard:

```yaml
patches:
  - path: add-label.patch.json
    target:
      group: apps
      version: v1
      kind: Deployment
```

```json
[
  {"op": "add", "path": "/metadata/labels/app.kubernetes.io~1version", "value": "1.21.0"}
]
```

Gotcha: a special replacement character `~1` is used for `/` in a label name, so the label `app.kubernetes.io/version` is written `app.kubernetes.io~1version` in the path.

Kubernetes task page example: `- op: replace` with `path: /spec/replicas` and `value: 3`, with `target` of `group: apps`, `version: v1`, `kind: Deployment`, `name: my-nginx` and `path: patch.yaml`. The task page notes JSON6902 is for fields or resources that strategic merge patches do not support.

## Checked

2026-11-08: read the kustomize patches reference page and the Kubernetes kustomize task page in full; confirmed the inline and path examples, mandatory target, `~1` escape, YAML or JSON file content and the replicas example. Removed the warning that reordering containers silently retargets index-based patches, which neither page states.

Method: documentation only; no commands were run.
