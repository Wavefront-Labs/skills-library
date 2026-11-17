---
id: computing-software.devops-ci-cd.flux.kustomization-apply-annotations
name: kustomization-apply-annotations
category: computing-software
field: devops-ci-cd
product: flux
tags: [kustomization, ssa, merge, ifnotpresent, force]
level: advanced
status: docs-checked
description: "Per-object annotations that change how kustomize-controller applies, recreates or prunes a resource, and spec.force."
sources:
  - https://fluxcd.io/flux/components/kustomize/kustomizations/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Annotate objects in the source manifests to change how kustomize-controller treats them:

- `kustomize.toolkit.fluxcd.io/ssa` (default `Override`): apply policy.
  - `Override`: reconcile to the Git state; manual `kubectl edit` changes are reverted. To keep fields added by `kubectl`, use `--field-manager=flux-client-side-apply`.
  - `Merge`: keep fields other tools added, as long as they do not overlap the desired state. Atomic lists such as `.spec.tolerations` still get reverted.
  - `IfNotPresent`: apply only if the object does not exist, for objects other controllers mutate, such as cert-manager Secrets or ValidatingWebhookConfigurations.
  - `Ignore`: never apply it, even though it is in the source.
- `kustomize.toolkit.fluxcd.io/force`: `Enabled` recreates just that object when an immutable field changes.
- `kustomize.toolkit.fluxcd.io/prune`: `Disabled` keeps the object when it leaves the source.

```yaml
metadata:
  annotations:
    kustomize.toolkit.fluxcd.io/ssa: Merge
```

`.spec.force: true` on the whole Kustomization replaces any object whose patch fails on immutable fields. Enable it temporarily, for example when changing Deployment pod selectors, because force-replacing can cause downtime. The per-object force annotation is safer; remove it once applied.

## Checked

2026-11-03. Read the Kustomization reference (fluxcd.io/flux/components/kustomize/kustomizations/): `kustomize.toolkit.fluxcd.io/ssa` values and defaults, Merge and atomic lists, IfNotPresent, Ignore, `force` and `prune` annotations, `.spec.force` downtime warning and `--field-manager=flux-client-side-apply`. Removed an unsupported closing sentence.

Method: documentation only; no commands were run.
