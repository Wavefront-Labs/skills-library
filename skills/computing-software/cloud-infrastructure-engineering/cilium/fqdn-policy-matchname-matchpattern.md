---
id: computing-software.cloud-infrastructure-engineering.cilium.fqdn-policy-matchname-matchpattern
name: fqdn-policy-matchname-matchpattern
category: computing-software
field: cloud-infrastructure-engineering
product: cilium
tags: [cilium, tofqdns, matchname, matchpattern, dns-proxy, wildcards]
level: advanced
status: docs-checked
description: "Allow egress by DNS name with Cilium toFQDNs matchName and matchPattern wildcards, DNS proxy requirements and combination limits."
sources:
  - https://docs.cilium.io/en/stable/security/policy/layer3/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# DNS-based (toFQDNs) policy

For non-cluster peers with changing IPs. Cilium intercepts DNS responses per endpoint with the DNS proxy, which requires `--enable-l7-proxy=true` and an L7 policy allowing DNS requests (a `rules.dns` block). A CIDR rule is generated for every `toFQDNs` rule, using IPs from all DNS responses seen on the node.

Selectors:
- `toFQDNs.matchName`: exact domain; multiple entries allowed.
- `toFQDNs.matchPattern`: letters a-z, 0-9, `.` and `-` plus `*`. `*` inside a label matches zero or more valid chars except `.` (`*.cilium.io` matches `sub.cilium.io`, not `cilium.io` or `sub.sub.cilium.io`; `part*ial.com` matches `partial.com`). `*` alone matches all names. Prefix `**.` matches all nested subdomains (`**.cilium.io` matches `app.cilium.io` and `test.app.cilium.io`, not `cilium.io`).

Limits and gotchas:
- `toFQDNs` egress rules cannot hold other L3 rules (`toEndpoints`, `toCIDRs`), but may hold `toPorts` and an HTTP section.
- The DNS proxy lives in the agent, so DNS depends on agent pod availability.
- With a non-standard DNS port behind a Kubernetes Service, the port in the rule must match the backend port.
- For cluster-internal traffic use services or endpoints rules.

## Checked

2026-11-03. Claims were read against: https://docs.cilium.io/en/stable/security/policy/layer3/. 

Method: documentation only; no commands were run.
