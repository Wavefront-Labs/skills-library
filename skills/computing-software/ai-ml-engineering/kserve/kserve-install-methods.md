---
id: computing-software.ai-ml-engineering.kserve.kserve-install-methods
name: kserve-install-methods
category: computing-software
field: ai-ml-engineering
product: kserve
tags: [install, helm, kustomize, kserve-crd, kserve-resources, quick-install, addon-install, server-side, uninstall, defaultdeploymentmode]
level: practitioner
status: docs-checked
description: "Install the KServe controller with Kustomize, Helm OCI charts (kserve-crd, kserve-resources) or quick-install scripts, for Knative or Standard mode, plus uninstall."
sources: ["https://github.com/kserve/website/blob/main/docs/install/kserve-install.md", "https://github.com/kserve/website/blob/main/docs/install/dependencies.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Installing KServe (Kustomize, Helm, scripts)

Install the mode's dependencies first (see kserve-install-dependencies).

## Kustomize (from a clone of the kserve repo)
```bash
kubectl apply -k config/overlays/standalone/kserve   # Knative mode default
kubectl apply -k config/overlays/addons/kserve       # when LLMIsvc already installed
kubectl apply -k config/runtimes                     # ClusterServingRuntimes
```
For Standard mode edit `config/configmap/inferenceservice.yaml` so the `deploy` key is `{"defaultDeploymentMode": "Standard"}` before applying.

## Helm (OCI charts)
```bash
helm install kserve-crd oci://ghcr.io/kserve/charts/kserve-crd \
  --version v0.20.0 --namespace kserve --create-namespace
helm install kserve-resources oci://ghcr.io/kserve/charts/kserve-resources \
  --version v0.20.0 --namespace kserve \
  --set kserve.controller.deploymentMode=Standard --wait
```
Use `deploymentMode=Knative` for serverless. For the addon case (LLMIsvc already present) set `kserve.createSharedResources=false`.

## Quick-install scripts
`hack/setup/quick-install/kserve-knative-mode-full-install-helm.sh` and `kserve-standard-mode-full-install-helm.sh` install dependencies plus KServe; release assets named `kserve-MODE-mode-full-install-with-manifests.sh` need no clone.

## Uninstall
```bash
helm uninstall kserve-runtime-configs -n kserve
helm uninstall kserve-resources -n kserve
helm uninstall kserve-crd -n kserve
kubectl delete -k config/overlays/standalone/kserve   # kustomize path
```
Scripts take `--uninstall`.

## Checked
Confirmed against KServe's install page: Kustomize overlays, Standard mode ConfigMap edit, Helm OCI charts at v0.20.0 with `deploymentMode`, addon `createSharedResources=false`, quick-install scripts and release scripts, uninstall commands and `--uninstall`.
Method: docs-only read of cited pages, 2026-11-08
