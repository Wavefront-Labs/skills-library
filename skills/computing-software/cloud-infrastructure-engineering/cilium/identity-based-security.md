---
id: computing-software.cloud-infrastructure-engineering.cilium.identity-based-security
name: identity-based-security
category: computing-software
field: cloud-infrastructure-engineering
product: cilium
tags: [cilium, identity, labels, security-identity, pod-labels, key-value-store]
level: practitioner
status: docs-checked
description: "Why Cilium enforces policy on label-derived identities instead of IP address filters, and how new pods only need an identity lookup."
sources:
  - https://docs.cilium.io/en/stable/security/network/identity/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Identity-based security

Problem with IP filters: if `role=frontend` pods may reach `role=backend` pods, every node with a backend pod needs a filter listing all frontend IPs. Each pod start or stop changes the lists on potentially thousands of nodes, and new frontend pods must wait until all backends are updated.

Cilium separates security from addressing. Security is based on a pod identity derived from labels and shared between pods with the same labels. When the first `role=frontend` pod starts it gets an identity allowed to reach the `role=backend` identity. Starting more frontend pods only requires resolving that identity through a key-value store; nothing changes on nodes hosting backends. The only delay is identity resolution.

Related: identity-relevant labels control how many identities get allocated; every unique label set (including fqdn selector labels) allocates its own numeric identity.

## Checked

2026-11-03. Claims were read against: https://docs.cilium.io/en/stable/security/network/identity/. 

Method: documentation only; no commands were run.
