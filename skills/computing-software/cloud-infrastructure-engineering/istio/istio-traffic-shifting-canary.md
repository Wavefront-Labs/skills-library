---
id: computing-software.cloud-infrastructure-engineering.istio.istio-traffic-shifting-canary
name: istio-traffic-shifting-canary
category: computing-software
field: cloud-infrastructure-engineering
product: istio
tags: [istio, traffic-shifting, weighted-routing, canary-release]
level: practitioner
status: docs-checked
description: "Gradually move traffic between service versions with weighted VirtualService routes, using the Istio traffic-shifting task steps."
sources: ["https://istio.io/latest/docs/tasks/traffic-management/traffic-shifting/", "https://istio.io/latest/docs/reference/config/networking/virtual-service/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Weighted routes let you migrate in steps. A destination's `weight` is a relative proportion: it receives weight / (sum of all weights) of requests, and a weight of 0 receives nothing when there are several destinations. The task steps 100% v1, then 50/50, then 100% v3.

```yaml
http:
- route:
  - destination: {host: reviews, subset: v1}
    weight: 90
  - destination: {host: reviews, subset: v3}
    weight: 10
```

Apply, watch the new version, then edit the weights. The Gateway API equivalent is an `HTTPRoute` whose `backendRefs` each carry a `weight` (the task uses Services `reviews-v1` and `reviews-v3`).

Gotchas: the split is statistical per request; the task says you may need to refresh 15 or more times to see the distribution. Wait a few seconds for rules to propagate after each change. For an HTTPRoute the task shows `status.parents` conditions with `type: Accepted` and `status: "True"` (message "Route was valid"). Version shifting with Istio weights is independent of instance scaling, so the two versions can scale separately without changing the split.

## Checked

2026-11-03. Confirmed against the Istio Traffic Shifting task (50/50 then 100% v3 rules, HTTPRoute backendRefs with weight, Accepted condition, refresh and propagation remarks) and the VirtualService reference (`weight` semantics). Real error fixed: the draft said weights must sum to 100, but the reference defines them as relative proportions. Removed: invented curl loop, `istioctl proxy-config route` check and the sticky-session claim.
Method: documentation only; no commands were run.
