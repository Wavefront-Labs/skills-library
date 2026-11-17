---
id: computing-software.ai-ml-engineering.kserve.kserve-llmisvc-install
name: kserve-llmisvc-install
category: computing-software
field: ai-ml-engineering
product: kserve
tags: [llmisvc, llminferenceservice, kserve-llmisvc-crd, kserve-llmisvc-resources, kserve-runtime-configs, llmisvcconfigs, createsharedresources, lws, envoy-gateway, gateway-api]
level: practitioner
status: docs-checked
description: "Install the LLMInferenceService controller: prerequisites (Gateway API, Envoy AI Gateway, LWS), Kustomize overlays, three Helm OCI charts, createSharedResources=false, uninstall."
sources: ["https://github.com/kserve/website/blob/main/docs/install/llmisvc-install.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# LLMInferenceService installation

Prerequisites: cert-manager, Gateway API CRDs plus extension CRDs, Envoy Gateway, Envoy AI Gateway, Gateway API resources (GatewayClass, Gateway), the LWS operator (LeaderWorkerSet), and an external load balancer on local clusters.

## Kustomize (from a KServe repo clone)
```bash
kubectl apply -k config/overlays/standalone/llmisvc   # standalone
kubectl apply -k config/overlays/addons/llmisvc       # KServe already installed
kubectl apply -k config/llmisvcconfig                 # LLMInferenceServiceConfigs
```

## Helm (OCI charts, namespace `kserve`)
```bash
helm install kserve-llmisvc-crd oci://ghcr.io/kserve/charts/kserve-llmisvc-crd \
  --version v0.20.0 --namespace kserve --create-namespace
helm install kserve-llmisvc-resources oci://ghcr.io/kserve/charts/kserve-llmisvc-resources \
  --version v0.20.0 --namespace kserve --create-namespace --wait
helm install kserve-runtime-configs oci://ghcr.io/kserve/charts/kserve-runtime-configs \
  --version v0.20.0 --namespace kserve --set kserve.llmisvcConfigs.enabled=true
```

When KServe is already installed, add `--set kserve.createSharedResources=false` to the `kserve-llmisvc-resources` install to avoid conflicts.

The third chart installs the pre-configured LLMInferenceServiceConfig templates for common LLM frameworks.

## Scripts
`./hack/setup/quick-install/llmisvc-full-install-helm.sh` installs dependencies plus LLMIsvc; a `llmisvc-full-install-helm-with-manifest.sh` variant needs no clone (embedded manifests). Add `--uninstall` to the Helm script to remove everything (dependencies and LLMIsvc).

## Uninstall
`helm uninstall kserve-runtime-configs`, then `kserve-llmisvc-resources`, then `kserve-llmisvc-crd` (all `-n kserve`), or `kubectl delete -k config/overlays/standalone/llmisvc`.

Optional follow-up: install the LocalModel controller for model caching.

## Checked
Confirmed against the KServe LLMInferenceService Installation page: prerequisite list, the three Kustomize commands, the three Helm OCI installs with their flags and the addon createSharedResources=false variant, the quick-install scripts, and the Helm, Kustomize and script uninstall commands.

Method: docs-only read of cited pages, 2026-11-08
