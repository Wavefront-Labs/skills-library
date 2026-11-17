---
id: computing-software.cloud-infrastructure-engineering.istio.istio-minimal-profile-with-separate-gateways
name: istio-minimal-profile-with-separate-gateways
category: computing-software
field: cloud-infrastructure-engineering
product: istio
tags: [istio, minimal-profile, gateway-install]
level: practitioner
status: docs-checked
description: "Install only istiod with the minimal profile and manage ingress gateways as their own releases so gateway upgrades are decoupled from the control plane."
sources: ["https://istio.io/latest/docs/setup/additional-setup/config-profiles/", "https://istio.io/latest/docs/tasks/traffic-management/ingress/gateway-api/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
With the `minimal` profile the install contains the control plane only. That is the right base when you want gateways owned by application teams or when using the Kubernetes Gateway API, which auto-provisions a gateway deployment per `Gateway` object.

```sh
istioctl install --set profile=minimal -y
kubectl get crd gateways.gateway.networking.k8s.io >/dev/null 2>&1 || \
  echo "Gateway API CRDs missing - install them before creating Gateway objects"
```

Gotcha: the Gateway API CRDs are not installed on most clusters by default; install them before creating `Gateway` objects.

Verify: `kubectl get pods -n istio-system` shows only `istiod`; after creating a `Gateway` with `gatewayClassName: istio`, `kubectl wait -n <namespace> --for=condition=programmed gateways.gateway.networking.k8s.io <name>` succeeds.

## Checked

2026-11-03. Confirmed in the Istio configuration profiles page (`minimal` profile) and the Gateway API task (CRDs not installed by default, `gatewayClassName: istio`, `kubectl wait ... --for=condition=programmed`). Removed: the claim that the API server rejects Gateways without CRDs, the supported-version remark, and the namespace/RBAC advice (not on the pages read).

Method: documentation only; no commands were run.
