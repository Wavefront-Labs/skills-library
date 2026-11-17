---
id: computing-software.devops-ci-cd.kustomize.patch-target-selectors
name: patch-target-selectors
category: computing-software
field: devops-ci-cd
product: kustomize
tags: [patches, target, labelselector, annotationselector, regex]
level: practitioner
status: docs-checked
description: "Select patch targets by group, version, kind, name, namespace, labelSelector and annotationSelector; name and namespace are anchored regexes."
sources:
  - https://kubectl.docs.kubernetes.io/references/kustomize/kustomization/patches/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

A patch `target` selects resources by `group`, `version`, `kind`, `name`, `namespace`, `labelSelector` and `annotationSelector`. A resource that matches all the fields given has the patch applied; the page notes these are regular expressions.

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
```

Key points:

- `name` and `namespace` are automatically anchored: `myapp` is equivalent to `^myapp$`. To match a family, write the pattern yourself, such as `deploy.*`.
- Selectors combine with AND: every field you give must match.
- With a strategic merge patch and a `target`, the `metadata.name` inside the patch is required but not used; the doc's example uses `name: not-used`.
- For JSON6902 patches the `target` is always required.
- One patch with a label selector can touch many resources, for example every Deployment labelled `app.kubernetes.io/name=nginx`, which is the quickest way to set the same image or label on a group.

## Checked

2026-11-08: confirmed against the kustomize patches reference page, read in full (target fields, anchoring, not-used name, JSON6902 target requirement, label selector example). Removed the closing paragraph about selectors that match nothing, which that page does not address.

Method: documentation only; no commands were run.
