---
id: computing-software.devops-ci-cd.flux.kustomization-depends-on
name: kustomization-depends-on
category: computing-software
field: devops-ci-cd
product: flux
tags: [kustomization, dependson, ordering, crd, readiness]
level: sme
status: docs-checked
description: "Order Flux Kustomizations with spec.dependsOn so CRDs and controllers exist before the custom resources that use them."
sources:
  - https://fluxcd.io/flux/components/kustomize/kustomizations/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`.spec.dependsOn` lists other Kustomizations that must be Ready (condition `Ready` is `True` from the last applied status) before this one is applied. Use it when objects need others to exist first, for example CRDs and their controller before custom resources.

```yaml
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: cert-manager
  namespace: flux-system
spec:
  interval: 5m
  path: ./infra/cert-manager
  prune: true
  wait: true
  sourceRef:
    kind: GitRepository
    name: flux-system
---
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: certs
  namespace: flux-system
spec:
  interval: 5m
  path: ./infra/certs
  prune: true
  sourceRef:
    kind: GitRepository
    name: flux-system
  dependsOn:
    - name: cert-manager
```

If the upstream Kustomization has non-empty `healthChecks` or `wait: true`, the dependent Kustomization is applied only after those health checks pass.

Circular dependencies must be avoided, otherwise the interdependent Kustomizations are never applied. List Kustomizations and their readiness with `flux get kustomizations`.

## Checked

2026-11-03. Read the Kustomization reference (fluxcd.io/flux/components/kustomize/kustomizations/): `dependsOn` readiness from last applied status, health-check ordering, circular dependency warning; `flux get kustomizations` checked on the Flux CLI page. Removed unsupported statements about Ready semantics without health checks and status reporting of waiting.

Method: documentation only; no commands were run.
