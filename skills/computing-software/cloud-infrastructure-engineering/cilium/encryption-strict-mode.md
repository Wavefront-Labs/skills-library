---
id: computing-software.cloud-infrastructure-engineering.cilium.encryption-strict-mode
name: encryption-strict-mode
category: computing-software
field: cloud-infrastructure-engineering
product: cilium
tags: [cilium, strict-mode, encryption-strictmode, egress, ingress, unencrypted-leak]
level: advanced
status: docs-checked
description: "Prevent unencrypted leaks with Cilium encryption.strictMode egress cidr and ingress, and their IPv4, routing and interface limitations."
sources:
  - https://docs.cilium.io/en/stable/security/network/encryption/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Transparent encryption known issue and strict mode

Problem: packets to a not-yet-discovered remote endpoint or new remote node may leave unencrypted, because Cilium has to assume the destination is outside the cluster until it learns otherwise.

Mitigations:
1. Egress policy that disallows traffic to `reserved:world` or restricts outside access to trusted targets with `toCIDR`, `toCIDRSet`, `toFQDN`.
2. Strict mode egress: `encryption.strictMode.egress.enabled=true` and `encryption.strictMode.egress.cidr` set to the pod CIDR. Traffic leaving a node to that CIDR is always encrypted; new pod endpoint info must still propagate first. Limits: the CIDR must be IPv4 (IPv6 is not protected and can leak); to disable all dynamic lookups use direct routing with non-overlapping node and pod CIDRs, otherwise set `encryption.strictMode.egress.allowRemoteNodeIdentities=true`, which allows unencrypted traffic from or to node-identity IPs.
3. Strict mode ingress: `encryption.strictMode.ingress.enabled`. Drops cluster-internal ingress not arriving through the WireGuard tunnel. Works in tunnel and native routing but needs WireGuard (not IPsec). Limits: node-to-node WireGuard traffic is not covered; BPF must be attached to every pod-routable interface or an attacker could inject via an unmanaged interface; unsupported when chaining on other CNI plugins (GitHub issue 15596).

## Checked

2026-11-03. Claims were read against: https://docs.cilium.io/en/stable/security/network/encryption/. 

Method: documentation only; no commands were run.
