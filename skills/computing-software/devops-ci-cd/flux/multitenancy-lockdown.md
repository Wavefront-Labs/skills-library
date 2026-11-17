---
id: computing-software.devops-ci-cd.flux.multitenancy-lockdown
name: multitenancy-lockdown
category: computing-software
field: devops-ci-cd
product: flux
tags: [multitenancy, no-cross-namespace-refs, default-service-account, no-remote-bases, rbac]
level: advanced
status: docs-checked
description: "Lock Flux down for multi-tenant clusters with controller flags and impersonation so tenants cannot cross namespaces."
sources:
  - https://fluxcd.io/flux/installation/configuration/multitenancy/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
By default Flux controllers run as cluster-admin, fine when all users are trusted. For tenants, platform admins patch the controllers at bootstrap (see bootstrap customization) with these flags:

```yaml
patches:
  - patch: |
      - op: add
        path: /spec/template/spec/containers/0/args/-
        value: --no-cross-namespace-refs=true
    target:
      kind: Deployment
      name: "(kustomize-controller|helm-controller|notification-controller|image-reflector-controller|image-automation-controller|source-watcher)"
  - patch: |
      - op: add
        path: /spec/template/spec/containers/0/args/-
        value: --no-remote-bases=true
    target:
      kind: Deployment
      name: "kustomize-controller"
  - patch: |
      - op: add
        path: /spec/template/spec/containers/0/args/-
        value: --default-service-account=default
    target:
      kind: Deployment
      name: "(kustomize-controller|helm-controller|source-watcher)"
```

Effects:
- No cross-namespace references, so a tenant cannot use another tenant sources or subscribe to their events.
- No remote Kustomize bases, so only Flux sources affect cluster state.
- Kustomizations and HelmReleases without `spec.serviceAccountName` use the `default` account of their own namespace, which has no permissions; tenants must name a ServiceAccount.
- Also patch the `flux-system` Kustomization to run as a cluster-admin ServiceAccount (`/spec/serviceAccountName`: `kustomize-controller`), so admins can still create tenant namespaces and RBAC.

`source-watcher` supports `--default-service-account` only from Flux v2.10.0; remove it from that target on older versions or it fails with an unknown flag error.

Flux aggregates its CRDs into the built-in `view`, `edit` and `admin` roles; delete the `flux-view` and `flux-edit` ClusterRoles by patch if you want to disable that. The fluxcd/flux2-multi-tenancy repository is the reference example.

## Checked

2026-11-08. Read in full: https://fluxcd.io/flux/installation/configuration/multitenancy/ (raw source in the fluxcd/website repository).

Method: documentation only; no commands were run.
