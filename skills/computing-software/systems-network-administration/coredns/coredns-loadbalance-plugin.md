---
id: computing-software.systems-network-administration.coredns.coredns-loadbalance-plugin
name: coredns-loadbalance-plugin
category: computing-software
field: systems-network-administration
product: coredns
tags: [coredns, loadbalance, round-robin, weighted, prefer]
level: practitioner
status: docs-checked
description: "Shuffle A, AAAA and MX records, prefer subnets or use a weight file with the loadbalance plugin."
sources:
  - https://coredns.io/plugins/loadbalance/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: spread clients across multiple addresses.

Syntax:

```
loadbalance [round_robin | weighted WEIGHTFILE] {
    reload DURATION
    prefer CIDR [CIDR...]
}
```

- `round_robin` is the default: it randomises the order of A, AAAA and MX records with uniform probability. CNAMEs are sorted before address records because some stub resolvers such as glibc require it.
- `weighted WEIGHTFILE` assigns weights to IPs so that particular IPs are more likely to be the first A or AAAA record. It does not shuffle the whole answer, only that first record.
- `prefer CIDR...` reorders A and AAAA records so addresses in preferred subnets come first.
- `reload DURATION` rescans the weight file; default 30s; `0s` disables. A relative WEIGHTFILE path is prefixed with the root plugin path.

Weight file format: a domain name line followed by `ip weight` lines, with `#` comments. Weights range from 1 to 255.

```
www.example.org
192.0.2.1 100
192.0.2.2 50
```

Example in the docs: `loadbalance round_robin` in front of a forward to Google Public DNS.

## Checked

2026-11-03. Page read: https://coredns.io/plugins/loadbalance/ (the CoreDNS plugin page).

Confirmed: the syntax, options, defaults, limits, metric names and examples stated in this skill.

Removed or corrected: nothing.

Method: documentation only; no commands were run.
