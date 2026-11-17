---
id: computing-software.cloud-infrastructure-engineering.cilium.dns-l7-policy-and-proxy
name: dns-l7-policy-and-proxy
category: computing-software
field: cloud-infrastructure-engineering
product: cilium
tags: [cilium, dns-policy, matchname, matchpattern, dns-proxy, kube-dns, tofqdns]
level: advanced
status: docs-checked
description: "Allow or deny DNS queries with Cilium L7 DNS rules, restrict interception to cluster DNS, and pair with toFQDNs; includes search-list and port-range caveats."
sources:
  - https://docs.cilium.io/en/stable/security/policy/layer7/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# DNS L7 policy and the DNS proxy

Policy on query names (other DNS fields like query type are ignored) is enforced by the agent DNS proxy, which also feeds IPs to `toFQDNs` rules. DNS responses are cached in the agent respecting TTL. For a domain, IPs from responses to all pods on that Cilium instance are allowed (respecting TTLs). The proxy is the only way to get IPs from wildcard `matchPattern` DNS rules into `toFQDNs`.

Rules: `matchName` (exact) and `matchPattern` (a-z, 0-9, `.`, `-`, `*`). `*` within a label matches zero or more valid chars except `.`; `*` alone matches all names and inserts all response IPs into the agent DNS cache.

Docs example: DNS policy allows `cilium.io`, subdomains of cilium.io, and subdomains of `api.cilium.io`; a separate L3 `toFQDNs` rule lets connections go to returned IPs. A query for a name not covered by `toFQDNs` is answered but connections to its IPs are not allowed.

## Warnings
- Strongly prefer intercepting DNS only to the cluster DNS service such as kube-dns; intercepting other resolvers lets less-trusted servers influence IPs learned for toFQDNs.
- Any L7 rule with its L3/L4 parts blocks other traffic.
- In Kubernetes, allow `service.namespace.svc.cluster.local.` with `matchPattern: *.*.svc.cluster.local.`; names completed via the search list must be allowed in their completed form.
- DNS policies do not support port ranges.
- Visibility-only: the `dns-visibility.yaml` example intercepts without blocking any DNS requests while allowing L3 to cilium.io, sub.cilium.io and its subdomains.

## Checked

2026-11-03. Claims were read against: https://docs.cilium.io/en/stable/security/policy/layer7/. 

Method: documentation only; no commands were run.
