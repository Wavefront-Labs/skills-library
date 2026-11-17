---
id: computing-software.cloud-infrastructure-engineering.linkerd.weighted-traffic-shifting-httproute
name: weighted-traffic-shifting-httproute
category: computing-software
field: cloud-infrastructure-engineering
product: linkerd
tags: [linkerd, traffic-shifting, httproute, canary, weights]
level: practitioner
status: docs-checked
description: "Shift traffic between two backends gradually by editing backendRef weights on an HTTPRoute whose parent is the Service."
sources:
  - https://linkerd.io/2.19/tasks/traffic-shifting/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Linkerd splits traffic with HTTPRoute (or GRPCRoute) backendRefs and weights. The older TrafficSplit resource from the SMI extension is still supported but gets no further development.

With a Service `bb` and a second Service `bb-v2` for the new version, start with a 90/10 split:

```yaml
apiVersion: policy.linkerd.io/v1beta2
kind: HTTPRoute
metadata:
  name: bb-route
  namespace: traffic-shift-demo
spec:
  parentRefs:
    - name: bb
      kind: Service
      group: core
      port: 8080
  rules:
    - backendRefs:
      - name: bb
        port: 8080
        weight: 90
      - name: bb-v2
        port: 8080
        weight: 10
```

The `parentRef` is the `bb` Service that the client talks to. Whenever a meshed client calls that Service it uses this route. The original Service appears again in `backendRefs` so that 90% of the traffic continues to it.

To finish the rollout, apply the same route with only `bb-v2` at weight 100. Keep tweaking the weights to shift traffic gradually, or shift back if it looks dicey, while watching success rate and latency with `linkerd viz stat`.

## Checked

2026-11-08. Confirmed against: https://linkerd.io/2.19/tasks/traffic-shifting/. HTTPRoute and GRPCRoute splitting, TrafficSplit note, the 90/10 route, the parentRef explanation, the final 100 weight route.

Removed or reworded: The 50/50 step and the unmeshed-callers statement (not on the cited page).

Method: documentation only; no commands were run.
