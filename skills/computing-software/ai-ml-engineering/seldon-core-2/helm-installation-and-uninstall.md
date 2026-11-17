---
id: computing-software.ai-ml-engineering.seldon-core-2.helm-installation-and-uninstall
name: helm-installation-and-uninstall
category: computing-software
field: ai-ml-engineering
product: seldon-core-2
tags: [seldon-core-2, installation, helm, helm-charts, seldon-core-v2-crds, seldon-core-v2-setup, seldon-core-v2-runtime, seldon-core-v2-servers, clusterwide, uninstall]
level: practitioner
status: docs-checked
description: "Install Seldon Core 2 with Helm: the CRDs, setup, runtime and servers charts into seldon-mesh, the clusterwide option, the certs chart, and the uninstall order."
sources: ["https://github.com/SeldonIO/seldon-core/blob/v2/docs-gb/getting-started/kubernetes-installation/helm.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Helm installation and uninstall

Helm charts live in `k8s/helm-charts` and are published as the `seldon-charts` repo added below.

## Charts
- `seldon-core-v2-crds`: cluster wide install of the custom resources.
- `seldon-core-v2-setup`: the manager, namespaced or clusterwide, plus default SeldonConfig and ServerConfig resources so runtimes and servers install easily.
- `seldon-core-v2-runtime`: a SeldonRuntime resource that creates the core components in a namespace.
- `seldon-core-v2-servers`: example Server resources.
- `seldon-core-v2-certs`: a default set of TLS certificates.

Install ecosystem components (Jaeger, Prometheus, Kafka) first; Kafka has its own steps.

## Install order
```bash
helm repo add seldon-charts https://seldonio.github.io/helm-charts
helm repo update seldon-charts
helm install seldon-core-v2-crds seldon-charts/seldon-core-v2-crds
kubectl create namespace seldon-mesh
helm install seldon-core-v2 seldon-charts/seldon-core-v2-setup --namespace seldon-mesh
helm install seldon-v2-runtime seldon-charts/seldon-core-v2-runtime --namespace seldon-mesh
helm install seldon-v2-servers seldon-charts/seldon-core-v2-servers --namespace seldon-mesh
```
Any namespace works; seldon-mesh is the illustration. By default the setup chart installs the operator namespaced, controlling only that namespace. Add `--set controller.clusterwide=true` to allow SeldonRuntimes in any namespace; this needs ClusterRoles, so your user needs the permissions. The servers chart installs 1 MLServer and 1 Triton, and must go in the same namespace as the runtime.

## Uninstall
Remove running models and pipelines first, then in order. Use the release names you installed with (the page installs the runtime as `seldon-v2-runtime` but its uninstall step writes `seldon-core-v2-runtime`; check `helm list -n seldon-mesh`):
```bash
helm uninstall seldon-v2-runtime --namespace seldon-mesh
helm uninstall seldon-core-v2 --namespace seldon-mesh
helm uninstall seldon-core-v2-crds
```

## Checked

2026-11-04. Confirmed against kubernetes-installation/helm.md (Seldon Core 2 docs, v2 branch): chart list, install commands, clusterwide flag and ClusterRoles, servers chart contents, uninstall order. Removed or corrected: claimed publish location; uninstall release name corrected to match install.

Method: documentation only; no commands were run.
