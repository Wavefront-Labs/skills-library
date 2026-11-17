---
id: computing-software.cloud-infrastructure-engineering.kubernetes.istio-egress-gateway-and-serviceentry
name: istio-egress-gateway-and-serviceentry
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, istio, serviceentry, istio-egress-gateway, egress-control, registry-only, service-mesh]
level: advanced
status: docs-checked
description: "Control mesh egress with Istio: REGISTRY_ONLY outbound policy, ServiceEntry for allowed hosts, routing TLS traffic through an egress gateway, and closing the bypass."
sources: ["https://istio.io/latest/docs/tasks/traffic-management/egress/egress-control/", "https://istio.io/latest/docs/tasks/traffic-management/egress/egress-gateway/", "https://istio.io/latest/docs/tasks/traffic-management/egress/wildcard-egress-hosts/", "https://istio.io/latest/docs/reference/config/networking/service-entry/", "https://istio.io/latest/docs/tasks/observability/logs/telemetry-api/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Istio egress gateway and ServiceEntry

## Step 1: block unknown destinations
```yaml
# IstioOperator / istiod values
meshConfig:
  outboundTrafficPolicy:
    mode: REGISTRY_ONLY        # default ALLOW_ANY passes everything
```
Sidecars now block calls to hosts that have no ServiceEntry or service in the registry; the Istio egress-control task shows HTTPS calls failing with curl exit code 35. Blocked traffic is identified by the cluster name `BlackHoleCluster` (for example `xds.cluster_name == 'BlackHoleCluster'` in a Telemetry access-log filter). Config changes can take a few seconds to propagate.

## Step 2: declare allowed external hosts
```yaml
apiVersion: networking.istio.io/v1
kind: ServiceEntry
metadata: {name: stripe, namespace: payments}
spec:
  hosts: [api.stripe.com]
  location: MESH_EXTERNAL
  resolution: DNS
  ports: [{number: 443, name: tls, protocol: TLS}]
  exportTo: ["."]              # only this namespace sees it
```
Use `exportTo` so one team's ServiceEntry does not open egress mesh-wide.

## Step 3: force it through the egress gateway
Install the gateway (`istioctl install --set components.egressGateways[0].name=istio-egressgateway --set components.egressGateways[0].enabled=true`, or the gateway Helm chart).
```yaml
apiVersion: networking.istio.io/v1
kind: Gateway
metadata: {name: egress-stripe, namespace: payments}
spec:
  selector: {istio: egressgateway}
  servers:
  - port: {number: 443, name: tls, protocol: TLS}
    hosts: [api.stripe.com]
    tls: {mode: PASSTHROUGH}
---
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata: {name: stripe-via-egress, namespace: payments}
spec:
  hosts: [api.stripe.com]
  gateways: [mesh, egress-stripe]
  tls:
  - match: [{gateways: [mesh], port: 443, sniHosts: [api.stripe.com]}]
    route: [{destination: {host: istio-egressgateway.istio-system.svc.cluster.local, port: {number: 443}}}]
  - match: [{gateways: [egress-stripe], port: 443, sniHosts: [api.stripe.com]}]
    route: [{destination: {host: api.stripe.com, port: {number: 443}}}]
```
For mTLS from sidecar to gateway use port 443 with `ISTIO_MUTUAL` on a DestinationRule
subset and a gateway server with `mode: ISTIO_MUTUAL`.

## Step 4: close the bypass
Istio cannot securely enforce that all egress flows through the egress gateway: if a pod
bypasses its sidecar (for example it is not injected), it reaches external hosts directly.
The Istio docs say to enforce this outside Istio, with a firewall or Kubernetes
NetworkPolicy that allows app egress only to the mesh (istio-system, DNS) and allows
internet egress only from the egress gateway pods. Without it, the egress gateway is a
convention, not a control.

## Verify
```bash
kubectl exec deploy/checkout -c app -- curl -sI https://api.stripe.com | head -1   # 2xx/4xx from Stripe
kubectl exec deploy/checkout -c app -- curl -sI https://example.com                # fails
kubectl logs -n istio-system deploy/istio-egressgateway | grep api.stripe.com       # passed through gateway
```

## Gotchas
- Wildcard hosts in a ServiceEntry cannot use `resolution: DNS`; direct access uses `NONE`, and routing a wildcard through an egress gateway needs the extra configuration in the wildcard-egress-hosts task.
- Ambient mode uses waypoints and different egress patterns; this recipe is sidecar mode.

## Checked
2026-10-26. Checked against the istio.io docs source (repository istio/istio.io, last commit 2026-10-23). Confirmed: `meshConfig.outboundTrafficPolicy.mode` values `ALLOW_ANY` (default) and `REGISTRY_ONLY`; blocked HTTPS calls fail with curl exit code 35; DNS resolution is recommended over NONE for ServiceEntry (NONE trusts the Host header); egress gateway install via `components.egressGateways[0].name` and `.enabled`; Gateway/VirtualService with TLS PASSTHROUGH and `sniHosts`; the docs state Istio cannot enforce egress-gateway use and recommend a firewall or Kubernetes NetworkPolicy; wildcard hosts cannot use DNS resolution; the Telemetry API doc uses `xds.cluster_name == 'BlackHoleCluster'` for blocked traffic. Removed as unconfirmed: the 502 response for HTTP, the `istioctl proxy-config cluster | grep BlackHoleCluster` check and the sidecar-exclusion annotation name.
Method: documentation only; no commands were run.
