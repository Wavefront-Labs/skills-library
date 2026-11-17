---
id: computing-software.devops-ci-cd.kustomize.sort-options
name: sort-options
category: computing-software
field: devops-ci-cd
product: kustomize
tags: [sortoptions, order, legacy, fifo, output]
level: advanced
status: docs-checked
description: "Control the order of resources in kustomize build output with sortOptions legacy or fifo, available in v5.0.0 and later."
sources:
  - "https://kubectl.docs.kubernetes.io/references/kustomize/kustomization/sortoptions/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`sortOptions` sets how kustomize sorts the output at the end of a build (kustomize v5.0.0+). It replaces the deprecated `--reorder` CLI flag.

IMPORTANT: only the top-level Kustomization (the immediate target of `kustomize build`) is respected; instances in bases further down the chain are ignored.

```yaml
kind: Kustomization
sortOptions:
  order: legacy | fifo   # "legacy" is the default
```

- `fifo`: keeps resources in the order they are loaded in `resources`.
- `legacy` (default): uses two priority lists, `orderFirst` and `orderLast`; resources not listed sort between them by `apiVersion` and `kind`.

Customizing the legacy lists:

```yaml
sortOptions:
  order: legacy
  legacySortOptions:
    orderFirst:
    - Namespace
    orderLast:
    - Deployment
```

With no lists specified, the default `orderFirst` list is Namespace, ResourceQuota, StorageClass, CustomResourceDefinition, ServiceAccount, PodSecurityPolicy, Role, ClusterRole, RoleBinding, ClusterRoleBinding, ConfigMap, Secret, Endpoints, Service, LimitRange, PriorityClass, PersistentVolume, PersistentVolumeClaim, Deployment, StatefulSet, CronJob, PodDisruptionBudget; the default `orderLast` is MutatingWebhookConfiguration and ValidatingWebhookConfiguration.

Use `fifo` when your apply tool or a human reviewer expects the order you wrote.

## Checked

2026-11-03. Confirmed against: the sortOptions reference page.
Removed or reworded: nothing needed removing; all claims matched the pages.

Method: documentation only; no commands were run.
