---
id: computing-software.devops-ci-cd.kustomize.labels-field
name: labels-field
category: computing-software
field: devops-ci-cd
product: kustomize
tags: [labels, pairs, selectors, includeselectors]
level: practitioner
status: docs-checked
description: "The labels field adds labels to all resources without touching selectors by default; includeSelectors, includeTemplates and includeVolumeClaimTemplates widen the scope."
sources:
  - "https://kubectl.docs.kubernetes.io/references/kustomize/kustomization/labels/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`labels` adds labels without also automatically injecting corresponding selectors. It can be used instead of the deprecated `commonLabels`, which always adds selectors.

```yaml
labels:
- pairs:
    someName: someValue
    owner: alice
    app: bingo
  includeSelectors: true            # false by default
  includeTemplates: true            # false by default
  includeVolumeClaimTemplates: true # false by default
```

Flags (all false by default):

- `includeSelectors` applies labels to `metadata/labels`, selectors and `spec/template/metadata/labels`.
- `includeTemplates` applies labels to `metadata/labels` and `spec/template/metadata/labels` without modifying selectors; useful for labelling Pods of Deployments and StatefulSets.
- `includeVolumeClaimTemplates` applies to `metadata/labels` and `spec/volumeClaimTemplates/metadata/labels`, to label PersistentVolumeClaims from a StatefulSet.

Default behavior only labels `metadata.labels` of each resource.

Warning from the page: selectors for Deployments and Services should not change once applied to a cluster. Changing `includeSelectors` to true, or changing labels while it is true, on live resources is equivalent to changing `commonLabels` and could fail.

Task-page example: `labels: - pairs: {app: bingo}` with `includeSelectors: true`.

## Checked

2026-11-03. Confirmed against: the labels reference page and the task page.
Removed or reworded: nothing needed removing; all claims matched the pages.

Method: documentation only; no commands were run.
