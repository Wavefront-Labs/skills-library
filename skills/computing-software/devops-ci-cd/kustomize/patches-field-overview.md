---
id: computing-software.devops-ci-cd.kustomize.patches-field-overview
name: patches-field-overview
category: computing-software
field: devops-ci-cd
product: kustomize
tags: [patches, strategic-merge, json6902, target]
level: practitioner
status: docs-checked
description: "The patches field applies strategic merge or JSON6902 patches, from files or inline strings, to one or many selected resources, in listed order."
sources:
  - "https://kubectl.docs.kubernetes.io/references/kustomize/kustomization/patches/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`patches` is the recommended way to add or override fields. The list is applied in the order written. Each patch may be:

- a strategic merge patch or a JSON6902 patch,
- a file (`path`) or an inline string (`patch`),
- aimed at one resource or many, through `target`.

```yaml
patches:
- path: patch.yaml
  target:
    group: apps
    version: v1
    kind: Deployment
    name: deploy.*
    labelSelector: "env=dev"
    annotationSelector: "zone=west"
- patch: |-
    - op: replace
      path: /some/existing/path
      value: new value
  target:
    kind: MyKind
    labelSelector: "env=dev"
```

Small patches that do one thing are easier to review and mix in overlays; the same advice appears on the Kubernetes task page, which splits a replica increase and a memory limit into two patch files.

If `target` is omitted on a strategic merge patch, the resource is matched using apiVersion, kind and name from the patch itself. The Kubernetes task page says matching uses group, version, kind and name from the patch file.

Prefer `patches` over the deprecated `patchesStrategicMerge` and `patchesJson6902`; `kustomize edit fix` converts them.

## Checked

2026-11-03. Confirmed against: the patches reference page and the Kubernetes kustomization task page.
Removed or reworded: nothing needed removing; all claims matched the pages.

Method: documentation only; no commands were run.
