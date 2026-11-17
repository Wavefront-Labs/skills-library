---
id: computing-software.cloud-infrastructure-engineering.cilium.cidr-policies
name: cidr-policies
category: computing-software
field: cloud-infrastructure-engineering
product: cilium
tags: [cilium, fromcidr, tocidr, cidrset, ciliumcidrgroup, identities]
level: advanced
status: docs-checked
description: "Write Cilium CIDR policies with fromCIDR, toCIDRSet and except blocks, know when CIDR rules apply, and reduce identity use with CiliumCIDRGroup."
sources:
  - https://docs.cilium.io/en/stable/security/policy/layer3/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# CIDR-based policy

For peers without Cilium labels: external services, VMs, bare metal. Apply at ingress or egress.

Fields:
- Ingress `fromCIDR`; `fromCIDRSet` (with optional per-prefix subnet exceptions, also referencing a `CiliumCIDRGroup`).
- Egress `toCIDR`; `toCIDRSet` (same options). Endpoints selected by `fromEndpoints` are automatically allowed to reply.

CIDR rules apply only when Cilium cannot map a side to a label-derived identity: peers outside the cluster, the host network namespace, in-cluster-prefix IPs not networked by Cilium, and optionally node IPs. They do NOT apply when both sides are Cilium-managed or node IPs (incl. host-network pods); use labels, services or entities there.

Docs example (`cidr.yaml`): `app=myService` may reach 20.1.1.1 and 10.0.0.0/8 but not 10.96.0.0/12.

## Scalability
Many distinct CIDRs cause many security identities allocated per agent. Use a `CiliumCIDRGroup` to reduce identity usage.

## Checked

2026-11-03. Claims were read against: https://docs.cilium.io/en/stable/security/policy/layer3/. 

Method: documentation only; no commands were run.
