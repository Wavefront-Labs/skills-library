---
id: computing-software.cloud-infrastructure-engineering.linkerd.egress-network-traffic-policy
name: egress-network-traffic-policy
category: computing-software
field: cloud-infrastructure-engineering
product: linkerd
tags: [linkerd, egress, egressnetwork, tlsroute, policy]
level: advanced
status: docs-checked
description: "Describe outside destinations with EgressNetwork, set Allow or Deny, and permit specific hosts with a TLSRoute."
sources:
  - https://linkerd.io/2.19/reference/egress-network/
  - https://linkerd.io/2.19/features/egress/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
An `EgressNetwork` describes destinations outside the cluster so Gateway API routes can attach policy to them. The sidecar enforces it, so no separate egress gateway is needed. It is not a strong security boundary on its own, because an actor who bypasses the sidecar bypasses these controls.

Fields:

- `networks`: list of `cidr` entries, each with an optional `except` list. If empty, the resource captures the entire address space except the in-cluster networks given by the install-time `clusterNetworks` value.
- `trafficPolicy`: required, `Allow` or `Deny`. With `Allow`, traffic passes even with no matching route. With `Deny`, traffic not matched by a route is refused.

EgressNetworks are namespaced and only affect clients in their namespace, except those in the global egress namespace, which affect all namespaces. Namespace-local resources win. The global namespace defaults to `linkerd-egress` and is configurable with the `egress.globalEgressNetworkNamespace` Helm value.

Example that blocks all external traffic except HTTPS to httpbin.org:

```yaml
apiVersion: policy.linkerd.io/v1alpha1
kind: EgressNetwork
metadata:
  namespace: linkerd-egress
  name: all-egress-traffic
spec:
  trafficPolicy: Deny
---
apiVersion: gateway.networking.k8s.io/v1alpha2
kind: TLSRoute
metadata:
  name: tls-egress
  namespace: linkerd-egress
spec:
  hostnames:
    - httpbin.org
  parentRefs:
    - name: all-egress-traffic
      kind: EgressNetwork
      group: policy.linkerd.io
      namespace: linkerd-egress
      port: 443
  rules:
    - backendRefs:
        - kind: EgressNetwork
          group: policy.linkerd.io
          name: all-egress-traffic
```

## Checked

2026-11-03. Confirmed against: https://linkerd.io/2.19/reference/egress-network/, https://linkerd.io/2.19/features/egress/.

Removed or reworded: Nothing.

Method: documentation only; no commands were run.
