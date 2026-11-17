---
id: computing-software.cloud-infrastructure-engineering.istio.istio-ambient-waypoint-proxy
name: istio-ambient-waypoint-proxy
category: computing-software
field: cloud-infrastructure-engineering
product: istio
tags: [istio, waypoint-proxy, ambient-l7, istioctl-waypoint]
level: practitioner
status: docs-checked
description: "Deploy a waypoint proxy per namespace or service so ambient mesh can enforce L7 routing and HTTP authorization, then bind workloads to it."
sources: ["https://istio.io/latest/docs/ambient/usage/waypoint/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
ztunnel only understands L4. HTTP-aware features (route rules, method/path authorization, fault injection) need a waypoint, an Envoy deployment created from a Gateway API `Gateway` with class `istio-waypoint`.

```sh
istioctl waypoint apply -n demo --enroll-namespace
kubectl get gtw waypoint -n demo
```

Gotchas: a waypoint only handles traffic addressed to services by default; the `istio.io/waypoint-for` label (set with `--for`) changes that. The `istio.io/use-waypoint` label records intent only: ztunnel sends traffic straight to the destination, so L7 policy never applies, when the named waypoint does not exist or has no address, or when the traffic type does not match (for example a request sent directly to a pod IP while the waypoint handles service traffic). A policy with a workload `selector` is enforced at L4 by ztunnel; a policy whose `targetRef` names the waypoint Gateway applies only to that waypoint. To make the waypoint mandatory, add an ALLOW AuthorizationPolicy with a workload selector that permits only the waypoint's identity (its service account is named after the Gateway).

Verify: `kubectl get gtw waypoint -n demo` shows the Gateway, and `kubectl get ns -L istio.io/dataplane-mode` shows the namespace labelled `ambient` before the waypoint is applied.

## Checked

2026-11-03. Confirmed in the ambient waypoint guide: `istioctl waypoint apply [--enroll-namespace] [--for]`, `gatewayClassName: istio-waypoint`, the `istio.io/waypoint-for` and `istio.io/use-waypoint` labels, the bypass conditions, selector versus `targetRef` enforcement point, and the require-waypoint policy pattern. Removed: `istioctl waypoint status` (not on the page), the version-dependent L7-at-ztunnel remark, the latency claim and sizing advice.

Method: documentation only; no commands were run.
