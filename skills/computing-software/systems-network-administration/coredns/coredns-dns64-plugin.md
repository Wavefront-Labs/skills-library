---
id: computing-software.systems-network-administration.coredns.coredns-dns64-plugin
name: coredns-dns64-plugin
category: computing-software
field: systems-network-administration
product: coredns
tags: [coredns, dns64, nat64, ipv6, aaaa]
level: advanced
status: docs-checked
description: "Synthesize AAAA records from A records for IPv6-only clients behind NAT64 using dns64 with custom prefix and translate_all."
sources:
  - https://coredns.io/plugins/dns64/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: let IPv6-only networks reach IPv4-only names.

When asked for AAAA records but only A records exist, dns64 synthesizes AAAA records from the A records. Synthesis is only done if the query arrived over IPv6. It is meant for IPv6-only networks with NAT64.

```
dns64 [PREFIX] {
    [translate_all]
    prefix PREFIX
    [allow_ipv4]
}
```

- Default prefix is the well-known `64:ff9b::/96`; a custom prefix can be given as the argument or with `prefix`.
- `translate_all` translates all queries, including responses that already have AAAA results.
- `allow_ipv4` permits translating queries that arrive over IPv4; the default is IPv6 only.

Examples:

```
. {
    dns64
}
. {
    dns64 64:1337::/96
}
. {
    dns64 {
        prefix 64:1337::/96
    }
}
```

The first applies to all queries that came over IPv6 with the default prefix; the second and third use a custom local prefix.

Warning from the page: `allow_ipv4` also translates queries from dual-stack clients, so a client that sends an AAAA query that would normally be NXDOMAIN gets a translated result.

## Checked

2026-11-03. Page read: https://coredns.io/plugins/dns64/ (the CoreDNS plugin page).

Confirmed: the syntax, options, defaults, limits, metric names and examples stated in this skill.

Removed or corrected: the unsourced operational-notes paragraph (replaced by the page's allow_ipv4 warning).

Method: documentation only; no commands were run.
