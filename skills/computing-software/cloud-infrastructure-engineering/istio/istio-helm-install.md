---
id: computing-software.cloud-infrastructure-engineering.istio.istio-helm-install
name: istio-helm-install
category: computing-software
field: cloud-infrastructure-engineering
product: istio
tags: [istio, istio-helm, helm, istio-base]
level: practitioner
status: docs-checked
description: "Install Istio as separate Helm releases (base, istiod, gateway) in the right order, with CRDs managed deliberately."
sources: ["https://istio.io/latest/docs/setup/install/helm/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Helm installs the base, istiod and gateway components as separate releases.

```sh
helm repo add istio https://blob.istio.io/istio-release/charts
helm install istio-base istio/base -n istio-system --create-namespace
helm install istiod istio/istiod -n istio-system --wait
helm install istio-ingress istio/gateway -n istio-ingress --create-namespace --wait
```

Gotchas: install order matters: the `base` chart holds the cluster-wide CRDs, which must be installed before the control plane, then `istiod`, then gateways. By design, deleting a chart with Helm does not delete the CRDs it installed, and deleting the Istio CRDs cascade-deletes every VirtualService, DestinationRule and AuthorizationPolicy, so do not remove them when uninstalling to reinstall.

Verify: `helm ls -n istio-system` lists `istio-base` and `istiod` as deployed, `helm status istiod -n istio-system` reports the release, and `kubectl get pods -n istio-system` shows istiod ready.

## Checked

2026-11-03. Confirmed in the Istio Helm install guide: the repo URL `https://blob.istio.io/istio-release/charts`, `--create-namespace`, base then istiod then `istio/gateway`, `helm ls`/`helm status`, CRD retention on chart deletion, and the CRD cascade-delete warning. Removed: the old `istio-release.storage.googleapis.com` repo URL (404 when fetched), `--set profile=default`, the `crds/` upgrade claim, `istioctl verify-install`, the gateway label remark and the CI advice.

Method: documentation only; no commands were run.
