---
id: computing-software.cloud-infrastructure-engineering.istio.istio-traffic-mirroring
name: istio-traffic-mirroring
category: computing-software
field: cloud-infrastructure-engineering
product: istio
tags: [istio, traffic-mirroring, shadow-traffic, mirror]
level: practitioner
status: docs-checked
description: "Copy a percentage of live requests to a second version with VirtualService mirror and mirrorPercentage, discarding responses safely."
sources: ["https://istio.io/latest/docs/tasks/traffic-management/mirroring/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Mirroring sends a copy of live requests to another destination; responses from the mirror are discarded.

```yaml
http:
- route: [{destination: {host: httpbin, subset: v1}, weight: 100}]
  mirror: {host: httpbin, subset: v2}
  mirrorPercentage: {value: 20.0}
```

Gotchas: if `mirrorPercentage` is absent, all traffic is mirrored. Mirrored requests are sent with their Host/Authority headers appended with `-shadow` (for example `cluster-1` becomes `cluster-1-shadow`). Mirroring is fire and forget: responses are discarded. Subsets need a DestinationRule defining them by label. With the Kubernetes Gateway API, use an `HTTPRoute` rule filter of type `RequestMirror` with a `requestMirror.backendRef`.

Verify as the task does: send a request, then check `kubectl logs deploy/httpbin-v1 -c httpbin` and `kubectl logs deploy/httpbin-v2 -c httpbin`; both show the request once mirroring is on, while the client only sees the v1 response.

## Checked

2026-11-03. Confirmed against the Istio Mirroring task: VirtualService `mirror` and `mirrorPercentage.value`, the default of mirroring everything when the field is absent, the `-shadow` suffix, fire-and-forget behaviour, the DestinationRule subsets, the `RequestMirror` HTTPRoute filter and the log check. Removed: unsourced advice on isolated state, low-percentage rollout and offline comparison.
Method: documentation only; no commands were run.
