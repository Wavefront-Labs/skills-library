---
id: computing-software.cloud-infrastructure-engineering.cilium.l4-port-policies
name: l4-port-policies
category: computing-software
field: cloud-infrastructure-engineering
product: cilium
tags: [cilium, toports, layer4, port-range, portprotocol, icmp-blocked]
level: practitioner
status: docs-checked
description: "Limit Cilium ingress and egress ports with toPorts, port ranges, named ports, protocol values, and implicit ICMP blocking once any L4 rule exists."
sources:
  - https://docs.cilium.io/en/stable/security/policy/layer4/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Layer 4 port policy

`toPorts` on ingress and egress takes `PortProtocol` entries:
- `port`: number, or a name like `http` or `http-8080`. `endPort` is ignored for named ports.
- `endPort`: numeric end of a range (docs example limits to TCP 80-444).
- `protocol`: `TCP`, `UDP` or ""/`ANY`. Matching on ICMP is not supported here.

Behaviour:
- With no L4 policy, an endpoint can send and receive on all ports and protocols including ICMP.
- Once any L4 policy exists, ICMP is blocked unless related to an allowed connection.
- L4 policy applies to ports after service port mapping.
- Layer 7 rules support port ranges, except DNS rules.
- L3 plus L4 combine: `role=frontend` to `role=backend` only on TCP 80; others cannot reach backend, and frontend cannot reach backend on other ports. CIDR plus L4 works the same way (`role=crawler` to 192.0.2.0/24 on TCP 80 only).

## Checked

2026-11-08. Read in full against the Cilium docs source (rst) of the Layer 4 policy page: https://docs.cilium.io/en/stable/security/policy/layer4/. Confirmed the PortProtocol fields, ICMP behaviour, port range note and the L3+L4 and CIDR+L4 examples stated above. Nothing was removed.

Method: documentation only; no commands were run.
