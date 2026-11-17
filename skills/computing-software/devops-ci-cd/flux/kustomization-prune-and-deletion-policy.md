---
id: computing-software.devops-ci-cd.flux.kustomization-prune-and-deletion-policy
name: kustomization-prune-and-deletion-policy
category: computing-software
field: devops-ci-cd
product: flux
tags: [kustomization, prune, garbage-collection, deletionpolicy, orphan]
level: sme
status: docs-checked
description: "Control garbage collection of a Flux Kustomization with spec.prune, the prune annotation and deletionPolicy values."
sources:
  - https://fluxcd.io/flux/components/kustomize/kustomizations/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`.spec.prune` is required. When `true`, objects applied earlier but missing from the current source revision are removed from the cluster, and deleting the Kustomization removes everything it applied. Removal runs in the background and does not block reconciliation. Which objects count is tracked in `.status.inventory`.

Exempt one object from pruning by labelling or annotating it in the manifest:

```yaml
kustomize.toolkit.fluxcd.io/prune: disabled
```

`.spec.deletionPolicy` decides what happens when the Kustomization object itself is deleted:
- `MirrorPrune` (default): resources are deleted if `prune` is `true`, orphaned if `false`.
- `Delete`: resources are deleted before the Kustomization goes away.
- `WaitForTermination`: deleted, then waits for them to leave etcd, bounded by `.spec.timeout`; on timeout it logs an error and lets the Kustomization be deleted.
- `Orphan`: leave the resources in place.

Use `Orphan` for special cases where the managed resources are removed by other means, for example deleting the namespace set in `.spec.targetNamespace`.

```yaml
spec:
  prune: true
  deletionPolicy: Orphan
```

`flux tree kustomization NAME` prints the resources reconciled by a Kustomization (a preview command).

## Checked

2026-11-03. Read the Kustomization reference (fluxcd.io/flux/components/kustomize/kustomizations/): prune semantics, background removal, `prune: disabled` annotation, `deletionPolicy` values and WaitForTermination timeout behaviour; `flux tree kustomization` checked on its CLI page. Removed the claimed hang on deletion and the prune-preview advice.

Method: documentation only; no commands were run.
