---
id: computing-software.devops-ci-cd.kustomize.labels-selector-safety
name: labels-selector-safety
category: computing-software
field: devops-ci-cd
product: kustomize
tags: [labels, selectors, immutability, deployment, includetemplates]
level: advanced
status: docs-checked
description: "Add labels to running workloads safely by using includeTemplates instead of includeSelectors, and know what happens to live selectors."
sources:
  - https://kubectl.docs.kubernetes.io/references/kustomize/kustomization/labels/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Selectors for resources such as Deployments and Services should not be changed once the resource has been applied to a cluster. The labels page warns that changing `includeSelectors` to true, or changing labels while it is true, on live resources is equivalent to changing the deprecated `commonLabels` and could result in failures.

Safe pattern to add labels to Pods of existing owners, as the page describes `includeTemplates`:

```yaml
labels:
- pairs:
    team: payments
  includeTemplates: true
```

The flags, all false by default:

- `includeSelectors`: applies labels to `metadata/labels`, selectors, and `spec/template/metadata/labels`.
- `includeTemplates`: applies labels to `metadata/labels` and `spec/template/metadata/labels`, without modifying selectors. Use it to label Pods from owners such as Deployments and StatefulSets.
- `includeVolumeClaimTemplates`: applies labels to `metadata/labels` and `spec/volumeClaimTemplates/metadata/labels`, to label PersistentVolumeClaims from owners such as StatefulSets.

Build output for `includeTemplates: true` (page Example 3): the Deployment gains the labels in `metadata.labels` and `spec.template.metadata.labels`, with no `spec.selector`; the Service gets labels only in `metadata.labels`.

By contrast `includeSelectors: true` (Example 2) additionally writes the labels into Service `spec.selector` and Deployment `spec.selector.matchLabels`.

With no flag set (Example 1), only `metadata.labels` change.

`includeVolumeClaimTemplates: true` (Example 4) writes the labels into the StatefulSet `spec.volumeClaimTemplates` metadata labels and `metadata.labels`.

## Checked

2026-11-08: read the kustomize labels reference page in full; confirmed the warning, the three flags and their defaults, and Examples 1 to 4. Removed the decision guide and the `kubectl diff -k` advice, which are not stated on the page.

Method: documentation only; no commands were run.
