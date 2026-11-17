---
id: computing-software.cloud-infrastructure-engineering.istio.istio-ambient-mode-install
name: istio-ambient-mode-install
category: computing-software
field: cloud-infrastructure-engineering
product: istio
tags: [istio, ambient-mode, ztunnel, istio-cni]
level: practitioner
status: docs-checked
description: "Install Istio ambient mode with the ambient profile (istiod, CNI, ztunnel) and enrol a namespace without sidecar injection."
sources: ["https://istio.io/latest/docs/ambient/install/istioctl/", "https://istio.io/latest/docs/ambient/install/helm/", "https://istio.io/latest/docs/ambient/usage/waypoint/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Ambient mode moves L4 mesh duties (mTLS, identity, basic telemetry) into a per-node `ztunnel` daemonset, with no sidecars. The `ambient` profile installs istiod, the Istio CNI node agent, and ztunnel.

```sh
istioctl install --set profile=ambient --skip-confirmation
kubectl get crd gateways.gateway.networking.k8s.io >/dev/null 2>&1 || \
  kubectl apply --server-side -f <gateway-api-crds.yaml>
kubectl label namespace demo istio.io/dataplane-mode=ambient
```

Gotchas: the install guide says to perform any platform-specific setup before installing, and the Gateway API CRDs are not installed on most clusters by default (hence the `kubectl apply --server-side` step). ztunnel and the CNI node agent are DaemonSets: the `cni` chart installs the node agent that redirects traffic between pods and ztunnel, and the `ztunnel` chart installs the ztunnel DaemonSet.

Verify: `kubectl get pods -n istio-system` lists `istio-cni-node` and `ztunnel` pods Running on each node.

## Checked

2026-11-03. Confirmed in the ambient istioctl install guide (`istioctl install --set profile=ambient --skip-confirmation`, platform-specific setup, Gateway API CRDs applied with `kubectl apply --server-side`), the ambient Helm guide (cni chart, ztunnel DaemonSet, `istio-cni-node` and `ztunnel` pods) and the waypoint guide (`istio.io/dataplane-mode: ambient` namespace label). Removed: the claim that running pods are captured without restart, the `gke` profile remark, `istioctl ztunnel-config workloads` and the `HBONE` verify step, and the rollback tip (none confirmed on the pages read).

Method: documentation only; no commands were run.
