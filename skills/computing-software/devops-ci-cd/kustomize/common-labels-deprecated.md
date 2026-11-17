---
id: computing-software.devops-ci-cd.kustomize.common-labels-deprecated
name: common-labels-deprecated
category: computing-software
field: devops-ci-cd
product: kustomize
tags: [commonlabels, deprecated, labels, edit-fix]
level: intro
status: docs-checked
description: "commonLabels, which always injects selectors, is deprecated in v5.0.0; use labels and run kustomize edit fix to convert."
sources:
  - "https://kubectl.docs.kubernetes.io/references/kustomize/kustomization/commonlabels/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`commonLabels` adds labels and selectors to all resources; if the label key already exists the value is overridden. It was deprecated in v5.0.0 in favor of `labels`.

```yaml
commonLabels:
  someName: someValue
  owner: alice
  app: bingo
```

With a Deployment and a Service, the build output puts the labels in `metadata.labels`, in the Service `spec.selector`, in the Deployment `spec.selector.matchLabels` and in `spec.template.metadata.labels`.

The field will never be removed from the `v1beta1` API, but it will not be in `v1`. At least two releases separate deprecation and removal of v1beta1 CLI support.

Convert automatically:

```bash
kustomize edit fix
```

The equivalent explicit form that keeps the old behavior:

```yaml
labels:
- pairs:
    someName: someValue
  includeSelectors: true
```

Selectors on applied resources should not change, so changing `commonLabels` on live resources can break them. Before migrating a live project, build before and after and diff, so the selector set is identical. Also see `commonAnnotations`, which is not deprecated.

## Checked

2026-11-03. Confirmed against: the commonLabels and labels reference pages.
Removed or reworded: nothing needed removing; all claims matched the pages.

Method: documentation only; no commands were run.
