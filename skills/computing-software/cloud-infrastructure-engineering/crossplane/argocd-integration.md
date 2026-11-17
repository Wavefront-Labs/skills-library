---
id: computing-software.cloud-infrastructure-engineering.crossplane.argocd-integration
name: argocd-integration
category: computing-software
field: cloud-infrastructure-engineering
product: crossplane
tags: [argo-cd, gitops, resource-tracking, health, argocd-cm]
level: practitioner
status: docs-checked
description: "Configure Argo CD for Crossplane: annotation tracking, health checks, exclusions and client QPS."
sources:
  - https://docs.crossplane.io/latest/guides/crossplane-with-argo-cd/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Use Argo CD 2.4.8 or later. Edit the `argocd-cm` ConfigMap in the `argocd` namespace.

1. Resource tracking must be annotation based:

```yaml
data:
  application.resourceTrackingMethod: annotation
```

2. Health checks. Provider and Crossplane kinds need custom Lua under `resource.customizations`, keyed `"*.upbound.io/*"` and `"*.crossplane.io/*"`. The script reports Healthy when the `Ready` condition is True, Degraded when `Synced` or `LastAsyncOperation` is False, and otherwise Progressing. Kinds with no status, such as ProviderConfig, Composition or CompositionRevision, are treated as Healthy. The `pkg.crossplane.io` Provider already has a built-in check.

3. Hide `ProviderConfigUsage` objects with `resource.exclusions`, using `"*"` as apiGroups to cover every provider. They are internal and clutter the UI.

4. With many CRDs, set the Application Controller env var `ARGOCD_K8S_CLIENT_QPS` to `300` (default 50). `ARGOCD_K8S_CLIENT_BURST` defaults to twice the QPS.

Excluding ProviderConfigUsage keeps the resource count low, since a growing number of resources and types can hurt Argo CD UI reactivity.

## Checked

Version advice, annotation tracking, Lua health logic (condition handling, no-status kinds), the built-in Provider check, the exclusion rule and the QPS and burst defaults confirmed on the Configuring Crossplane with Argo CD guide. Unsourced claims about label-tracking conflicts, controller restart and Applications stuck Progressing were removed.

Method: docs-checked 2026-11-09 against the raw Configuring Crossplane with Argo CD guide (docs repo, current content folder), read in full.
