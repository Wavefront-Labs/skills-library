---
id: computing-software.cloud-infrastructure-engineering.istio.istio-destinationrule-subsets
name: istio-destinationrule-subsets
category: computing-software
field: cloud-infrastructure-engineering
product: istio
tags: [istio, destinationrule-subsets, destinationrule, subsets]
level: practitioner
status: docs-checked
description: "Declare named service versions in a DestinationRule by pod label, and understand how subset and port-level traffic policies override each other."
sources: ["https://istio.io/latest/docs/reference/config/networking/destination-rule/", "https://istio.io/latest/docs/tasks/traffic-management/request-routing/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Subsets are named label selectors that let a VirtualService address a version of a service.

```yaml
apiVersion: networking.istio.io/v1
kind: DestinationRule
metadata: {name: reviews}
spec:
  host: reviews.shop.svc.cluster.local
  trafficPolicy: {tls: {mode: ISTIO_MUTUAL}}
  subsets:
  - {name: v1, labels: {version: v1}}
  - {name: v2, labels: {version: v2}}
```

Policy inheritance (from the reference): subsets inherit the DestinationRule-level `trafficPolicy`, and settings on a subset override the corresponding destination-level settings. Port-level settings (`portLevelSettings`) override destination-level settings and are not merged with them, so fields omitted at port level get defaults.

Gotchas: a VirtualService `subset` is only valid if a corresponding DestinationRule declares it. If mutual TLS is enabled in the mesh and a DestinationRule is applied without `tls.mode: ISTIO_MUTUAL`, the circuit-breaking task reports 503 errors. The Bookinfo task checks subsets with `kubectl get destinationrules -o yaml`.

## Checked

2026-11-03. Confirmed against the DestinationRule reference (subsets, labels, `trafficPolicy` inheritance and override, `portLevelSettings` override) and the Request Routing and Circuit Breaking tasks (503 without ISTIO_MUTUAL). Removed: unsourced claims that subset policies are inert before routing, that unknown hosts are ignored, and the auto-mTLS override; invented `istioctl x describe` and `proxy-config` verify steps; pod labelling advice.
Method: documentation only; no commands were run.
