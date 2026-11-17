---
id: computing-software.systems-network-administration.coredns.coredns-acl-plugin
name: coredns-acl-plugin
category: computing-software
field: systems-network-administration
product: coredns
tags: [coredns, acl, access-control, security, source-ip]
level: practitioner
status: docs-checked
description: "Allow, block, filter or drop DNS queries by source CIDR and query type with the acl plugin, with examples and metrics."
sources:
  - https://coredns.io/plugins/acl/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: restrict who can query which record types.

Syntax:

```
acl [ZONES...] {
    ACTION [type QTYPE...] [net SOURCE...]
}
```

Actions:
- `allow` (the default for unmatched queries): the query proceeds.
- `block`: returns REFUSED.
- `filter`: returns an empty NOERROR answer.
- `drop`: sends no response at all.

QTYPE `*` or an omitted type matches all types. SOURCE is a single IP or CIDR; `*` matches all addresses. ZONES defaults to the block's zones. The plugin can be used multiple times in a server block.

Rules are evaluated on the source IP in the TCP/UDP header, which differs from the real client behind a forwarding or recursive server or a source NAT.

Examples:

```
acl {
    allow net 192.168.1.0/24
    block net 192.168.0.0/16
}
acl {
    allow net 192.168.0.0/24 192.168.1.0/24
    block
}
acl a.example.org {
    block net 192.168.1.0/24
}
```

The first blocks 192.168.0.0/16 except 192.168.1.0/24; the second allows only two subnets; the third restricts one name.

Metrics: `coredns_acl_blocked_requests_total`, `..._filtered_...`, `..._allowed_...`, `..._dropped_...`.

## Checked

2026-11-08. Checked in full against the acl plugin README (coredns/coredns master, the source of coredns.io/plugins/acl). Syntax, actions, source-IP caveat, examples and four metrics match. Description no longer promises rule ordering.

Method: documentation only; no commands were run.
