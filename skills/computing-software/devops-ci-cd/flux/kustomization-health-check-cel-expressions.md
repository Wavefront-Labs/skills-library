---
id: computing-software.devops-ci-cd.flux.kustomization-health-check-cel-expressions
name: kustomization-health-check-cel-expressions
category: computing-software
field: devops-ci-cd
product: flux
tags: [kustomization, healthcheckexprs, cel, custom-resources, kstatus]
level: advanced
status: docs-checked
description: "Define custom readiness logic for custom resources with spec.healthCheckExprs CEL expressions in Kustomization or HelmRelease."
sources:
  - https://fluxcd.io/flux/components/kustomize/kustomizations/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Resources without kstatus support can still be health-checked with `.spec.healthCheckExprs`, a list of CEL expressions. Each item has:
- `apiVersion` (required): only the group is matched, so it applies to every served version.
- `kind` (optional): omit to cover all kinds in the group; a specific kind wins over a group-only entry.
- `current` (required): CEL returning `true` when the resource is ready.
- `inProgress` (optional): `true` while still reconciling.
- `failed` (optional): `true` when reconciliation failed.

Evaluation order is `inProgress`, then `failed`, then `current`. The first expression that is `true` decides the status.

Sketch for a SealedSecret (the resource is referenced from `healthChecks` and described by an expression):

```yaml
spec:
  healthChecks:
    - apiVersion: bitnami.com/v1alpha1
      kind: SealedSecret
      name: my-secret
      namespace: apps
  healthCheckExprs:
    - apiVersion: bitnami.com/v1alpha1
      kind: SealedSecret
      failed: status.conditions.filter(e, e.type == 'Synced').all(e, e.status == 'False')
      current: status.conditions.filter(e, e.type == 'Synced').all(e, e.status == 'True')
```

The same field exists on HelmRelease for objects it deploys. An expression that references fields the custom resource does not have makes the controller wait until the timeout; the reference suggests the CEL Playground for checking expressions and `has(...)` for field existence (`has(status)` errors if `status` does not yet exist).

## Checked

2026-11-03. Read the Kustomization reference (fluxcd.io/flux/components/kustomize/kustomizations/): `healthCheckExprs` fields, group-only apiVersion matching, kind precedence, evaluation order and the SealedSecret example. Replaced untested advice with the page's warning about nonexistent fields and the CEL Playground.

Method: documentation only; no commands were run.
