---
id: computing-software.devops-ci-cd.kustomize.replacements-select-reject
name: replacements-select-reject
category: computing-software
field: devops-ci-cd
product: kustomize
tags: [replacements, select, reject, regex]
level: advanced
status: docs-checked
description: "Pick replacement targets with select and drop some of them with reject, and avoid the AND versus OR trap in reject lists."
sources:
  - "https://kubectl.docs.kubernetes.io/references/kustomize/kustomization/replacements/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`select` chooses target resources (required); `reject` removes some of them from the selection. Both take `group`, `version`, `kind`, `name`, `namespace`, `labelSelector` and `annotationSelector`; string fields accept plain strings and regular expressions.

```yaml
replacements:
- sourceValue: "500m"
  targets:
  - select:
      kind: Job|Deployment   # regex to target several kinds
    fieldPaths:
    - spec.template.spec.containers.*.resources.limits.cpu
    options:
      create: true
```

The `reject` list is the subtle part:

```yaml
reject:
- kind: Deployment
  name: my-deploy
```

rejects only resources that are both a Deployment and named `my-deploy`, while

```yaml
reject:
- kind: Deployment
- name: my-deploy
```

rejects all Deployments and also all resources named `my-deploy`. Fields within one list entry are ANDed; separate entries are ORed. To reject two kinds, list them as separate entries:

```yaml
reject:
- kind: Deployment
- kind: StatefulSet
```

Reject overrules select. Verify a replacement by building and inspecting both the selected and the rejected objects, since an overly broad regex like `kind: Job|Deployment` also matches kinds you did not intend.

## Checked

2026-11-03. Confirmed against: the replacements reference page.
Removed or reworded: nothing needed removing; all claims matched the pages.

Method: documentation only; no commands were run.
