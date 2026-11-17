---
id: computing-software.ai-ml-engineering.kserve.kserve-upgrade-v0-17-helm-migration
name: kserve-upgrade-v0-17-helm-migration
category: computing-software
field: ai-ml-engineering
product: kserve
tags: [upgrade, v017, helm-upgrade, helmshresource-policy, metahelmshrelease-name, kserve-crd, kserve-localmodel-crd, kserve-resources, clusterservingruntime]
level: advanced
status: docs-checked
description: "Upgrading to KServe v0.17+: split Helm charts, why plain helm upgrade fails, the keep and release-name annotation procedure for CRDs and runtimes, upgrade order, verification."
sources: ["https://github.com/kserve/website/blob/main/docs/install/upgrade-guide.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Upgrading to v0.17 and later (Helm)

Before v0.17: `helm upgrade kserve-crd oci://ghcr.io/kserve/charts/kserve-crd --version <V> -n kserve`, then `helm upgrade kserve oci://ghcr.io/kserve/charts/kserve --version <V> -n kserve --reuse-values`; Kustomize: `kubectl apply --server-side -k "github.com/kserve/kserve/config/default?ref=v<V>"`.

From v0.17 the charts are restructured, so a plain `helm upgrade` does not work. Needs Helm 3.8+.
- CRD charts: `kserve-crd`, `kserve-localmodel-crd`, `kserve-llmisvc-crd`.
- `kserve-runtime-configs` (new) owns ClusterServingRuntimes and LLMIsvcConfigs.
- Resource charts: `kserve` renamed `kserve-resources` (still upgrade the release named `kserve`), plus `kserve-localmodel-resources`, `kserve-llmisvc-resources`.

Steps MUST run in this order or CRDs and ClusterServingRuntimes can be deleted. Test in non-production first and back up.

1. CRDs: annotate every kserve CRD `helm.sh/resource-policy=keep`; `helm upgrade -i kserve-crd`; for localmodel (and llmisvc) CRDs set `meta.helm.sh/release-name=kserve-localmodel-crd` (or `kserve-llmisvc-crd`) then `helm upgrade -i` that chart; finally remove the keep annotation (`helm.sh/resource-policy-`).
2. Runtimes: annotate ClusterServingRuntimes (and `llmisvconfig`) with keep; set `meta.helm.sh/release-name=kserve-runtime-configs`; `helm upgrade -i kserve-runtime-configs ... --set kserve.servingruntime.enabled=true --set kserve.llmisvcConfigs.enabled=<true if LLMIsvc>`; remove keep.
3. Controllers: `helm upgrade kserve oci://.../kserve-resources`, `helm upgrade -i kserve-localmodel-resources`, and for LLMIsvc `helm upgrade -i kserve-llmisvc-resources --set kserve.createSharedResources=false`.
4. Verify: `helm list -n kserve`, `kubectl get crd | grep kserve`, `kubectl get clusterservingruntime`, `kubectl get llminferenceserviceconfigs`. The guide also lists the expected Helm releases (kserve-crd, kserve-localmodel-crd and kserve-llmisvc-crd if used, kserve-runtime-configs, kserve-resources, plus the localmodel and llmisvc resource releases if used) and suggests `kubectl get pods -n kserve`.

## Checked
Confirmed against the KServe Upgrade Guide: pre-v0.17 Helm and Kustomize commands, the v0.17.0 chart restructuring and renames, the Helm 3.8+ requirement, the ordered keep/release-name annotation steps, the runtime-configs flags, the createSharedResources=false requirement and the verification commands.

Method: docs-only read of cited pages, 2026-11-08
