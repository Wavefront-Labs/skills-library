---
id: computing-software.cloud-infrastructure-engineering.cilium.l3-endpoint-ingress-egress-rules
name: l3-endpoint-ingress-egress-rules
category: computing-software
field: cloud-infrastructure-engineering
product: cilium
tags: [cilium, fromendpoints, toendpoints, egressdeny, empty-endpointselector, both-sides]
level: practitioner
status: docs-checked
description: "Write Cilium endpoint-based L3 ingress and egress allow rules, empty selector semantics, egressDeny precedence and the need for policy on both sides."
sources:
  - https://docs.cilium.io/en/stable/security/policy/layer3/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Endpoint-based L3 rules

- Ingress: an endpoint receives from another if an ingress rule selects it in `endpointSelector` and the source in `fromEndpoints`. Docs example allows `role=frontend` to `role=backend` (examples `l3/simple/l3.yaml`).
- Egress: `endpointSelector` selects the sender, `toEndpoints` the destination (`l3_egress.yaml`).
- An empty EndpointSelector selects all endpoints. Ingress allow-all is `ingress-allow-all.yaml`. For egress, an empty selector selects all endpoints in the CiliumNetworkPolicy namespace (default is `default`).
- Policy must be configured on BOTH sides. An allow-all ingress on a receiver does not mean senders egress policy permits it, and the reverse.
- `egressDeny` wins: if one matches, egress is denied even if `egress` rules would allow it.
- Any rule selecting the endpoint with an ingress or egress section puts it in default deny for that direction, so an otherwise empty section can lock down without whitelisting peers (`egress-default-deny.yaml`).

## Checked

2026-11-03. Claims were read against: https://docs.cilium.io/en/stable/security/policy/layer3/. 

Method: documentation only; no commands were run.
