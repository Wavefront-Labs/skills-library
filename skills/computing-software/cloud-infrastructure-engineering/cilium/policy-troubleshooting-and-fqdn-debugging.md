---
id: computing-software.cloud-infrastructure-engineering.cilium.policy-troubleshooting-and-fqdn-debugging
name: policy-troubleshooting-and-fqdn-debugging
category: computing-software
field: cloud-infrastructure-engineering
product: cilium
tags: [cilium, policy-troubleshooting, cilium-dbg, tofqdns, fqdn-cache, endpoint-get]
level: advanced
status: docs-checked
description: "Trace which policies apply to a Cilium endpoint with cilium-dbg endpoint get and policy get, and debug toFQDNs rules via fqdn cache list and ip list."
sources:
  - https://docs.cilium.io/en/stable/security/policy/troubleshooting/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Policy troubleshooting

## Which rules apply to an endpoint
Exec into the Cilium pod, then for endpoint 568:

```
cilium-dbg endpoint get 568 -o jsonpath='{range ..status.policy.realized.l4.ingress[*].derived-from-rules}{@}{"\n"}{end}'|tr -d '][' | xargs -I{} bash -c 'echo "Labels: {}"; cilium-dbg policy get {}'
```
Repeat with `...l4.egress[*]...`. The structure says "l4" but reflects L3, L4 and L7 policy. A rule without labels cannot be fetched alone: `cilium-dbg policy get` with no labels returns all policy on the node; rules with the same labels return together.

## toFQDNs
`toFQDNs` does nothing without an L7 DNS rule covering the endpoint (docs allow kube-dns on port 53 with `matchPattern: "*"`). Effects change as DNS data changes, so:
1. `cilium-dbg policy get` shows the imported FQDN policy.
2. After a DNS request, `cilium-dbg fqdn cache list` shows FQDN to IP mappings with TTLs.
3. `cilium-dbg ip list | grep <IP>` shows a local identity labeled `fqdn:<name>` plus `reserved:world`.

## Identity exhaustion
Each unique label combination allocates its own numeric identity. Watch metric `identity_label_sources{type="fqdn"}` against `fqdn_selectors`.

## Checked

2026-11-08. Read in full against the Cilium docs source (rst) of the policy troubleshooting page: https://docs.cilium.io/en/stable/security/policy/troubleshooting/. Confirmed the endpoint get and policy get workflow and the toFQDNs checks and identity metrics stated above. Nothing was removed.

Method: documentation only; no commands were run.
