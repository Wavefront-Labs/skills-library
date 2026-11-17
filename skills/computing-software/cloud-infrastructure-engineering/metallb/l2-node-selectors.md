---
id: computing-software.cloud-infrastructure-engineering.metallb.l2-node-selectors
name: l2-node-selectors
category: computing-software
field: cloud-infrastructure-engineering
product: metallb
tags: [metallb, l2-nodeselectors, nodeselectors, l2advertisement, layer2, subnet]
level: practitioner
status: docs-checked
description: "Restrict which nodes may announce a pool's IPs in L2 mode using nodeSelectors on L2Advertisement, for clusters where only some nodes sit on a given subnet."
sources:
  - https://raw.githubusercontent.com/metallb/metallb/main/website/content/configuration/_advanced_l2_configuration.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# L2 node selectors

Normally every node running a speaker is eligible to be the leader for any IP. When only some nodes are exposed to a network (the docs' diagram: NodeA and NodeB on subnet A, NodeC on subnet B), limit eligibility with `nodeSelectors` on the `L2Advertisement`:

```yaml
apiVersion: metallb.io/v1beta1
kind: L2Advertisement
metadata:
  name: example
  namespace: metallb-system
spec:
  ipAddressPools:
  - first-pool
  nodeSelectors:
  - matchLabels:
      kubernetes.io/hostname: NodeA
  - matchLabels:
      kubernetes.io/hostname: NodeB
---
apiVersion: metallb.io/v1beta1
kind: L2Advertisement
metadata:
  name: example
  namespace: metallb-system
spec:
  ipAddressPools:
  - second-pool
  nodeSelectors:
  - matchLabels:
      kubernetes.io/hostname: NodeC
```
IPs from `first-pool` are reachable only through NodeA or NodeB (one is elected). IPs from `second-pool` always use NodeC.

Notes:
- This is a hard filter. For a soft preference use `computing-software.cloud-infrastructure-engineering.metallb.l2-preferred-node-selectors`.
- The two example resources share a `name` in the docs; give each advertisement its own name when you apply them.

`kubectl get servicel2statuses -n metallb-system` lists the allocated node per Service (`computing-software.cloud-infrastructure-engineering.metallb.service-status-resources`).

## Checked
2026-11-04. Confirmed against the MetalLB "Advanced L2 configuration" page (node selector section, both YAML objects, diagram) and the FAQ (ServiceL2Status columns). Reworded the duplicate-name note without a claim about overwriting.
Method: documentation only; no commands were run.
