---
id: computing-software.devops-ci-cd.kustomize.cross-cutting-fields-example
name: cross-cutting-fields-example
category: computing-software
field: devops-ci-cd
product: kustomize
tags: [namespace, nameprefix, labels, annotations, deployment]
level: intro
status: docs-checked
description: "Combine namespace, namePrefix, nameSuffix, labels and commonAnnotations in one kustomization and see their effect on a Deployment."
sources:
  - https://kubernetes.io/docs/tasks/manage-kubernetes-objects/kustomization/
  - https://kubectl.docs.kubernetes.io/references/kustomize/kustomization/labels/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

The task page sets common fields for all resources in one project: the same namespace, name prefix or suffix, labels and annotations.

```yaml
namespace: my-namespace
namePrefix: dev-
nameSuffix: "-001"
labels:
  - pairs:
      app: bingo
    includeSelectors: true
commonAnnotations:
  oncallPager: 800-555-1212
resources:
- deployment.yaml
```

For a Deployment `nginx-deployment` labelled `app: nginx`, viewed with `kubectl kustomize ./`, the page shows:

- `metadata.name: dev-nginx-deployment-001`
- `metadata.namespace: my-namespace`
- `metadata.labels.app: bingo` (the original value `nginx` is replaced)
- `spec.selector.matchLabels.app: bingo` and `spec.template.metadata.labels.app: bingo`, since `includeSelectors: true`
- `oncallPager: 800-555-1212` under `metadata.annotations` and `spec.template.metadata.annotations`.

Lessons:

1. Selectors should not be changed once a resource has been applied to a cluster; the labels page warns that turning on `includeSelectors` or changing labels while it is on for live resources could result in failures.
2. Prefix, suffix and namespace are all applied in the same build.
3. Without `includeSelectors` (the default is false), `labels` adds labels without injecting selectors.

## Checked

2026-11-08: confirmed against the Kubernetes kustomize task page (cross-cutting fields example and output) and the kustomize labels reference page (includeSelectors default and warning). Removed the advice to set the label to the same value in the base and the note about quoting the suffix, which neither page states.

Method: documentation only; no commands were run.
