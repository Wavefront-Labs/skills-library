---
id: computing-software.systems-network-administration.coredns.coredns-forward-basics
name: coredns-forward-basics
category: computing-software
field: systems-network-administration
product: coredns
tags: [coredns, forward, upstream, proxy, resolver]
level: intro
status: docs-checked
description: "Proxy DNS queries to upstream resolvers with forward FROM TO, including protocols, the 15 upstream limit and hostname upstreams."
sources:
  - https://coredns.io/plugins/forward/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: send matching queries to one or more upstream resolvers.

Syntax: `forward FROM TO...`. FROM is the base domain to match, and `.` matches everything. TO is an endpoint with an optional protocol:
- `dns://` or no prefix for plain DNS
- `tls://9.9.9.9` for DNS over TLS
- `https://9.9.9.9` for DNS over HTTPS (default path /dns-query)
- a file such as a resolv.conf, or a hostname that is resolved to IPs at startup

Facts:
- The number of upstreams is limited to 15.
- Sockets to upstreams are re-used, and UDP, TCP, DoT and DoH are supported.
- Multiple upstreams are randomised on first use (see policy). If a healthy proxy returns an error during the exchange, the next upstream is tried.
- A FROM written in CIDR notation that expands to several reverse zones is not fully supported: only the first expanded zone is used.

Examples:

```
example.org {
    forward . 127.0.0.1:9005
}
. {
    forward . 10.0.0.10:53 10.0.0.11:1053 [2003::1]:53
}
```

The second balances across three resolvers, one with an IPv6 address.

## Checked

2026-11-03. Page read: https://coredns.io/plugins/forward/ (the CoreDNS plugin page).

Confirmed: the syntax, options, defaults, limits, metric names and examples stated in this skill.

Removed or corrected: nothing.

Method: documentation only; no commands were run.
