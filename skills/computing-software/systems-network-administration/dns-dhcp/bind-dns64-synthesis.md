---
id: computing-software.systems-network-administration.dns-dhcp.bind-dns64-synthesis
name: bind-dns64-synthesis
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dns, bind, bind-dns64, dns64, nat64, ipv6]
level: practitioner
status: docs-checked
description: "Configure DNS64 on BIND for IPv6-only clients behind NAT64: dns64 prefix, clients/exclude/mapped options, interaction with DNSSEC and testing."
sources:
  - https://www.rfc-editor.org/rfc/rfc6147
  - https://bind9.readthedocs.io/en/latest/reference.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DNS64 on BIND

DNS64 synthesises AAAA records from A records using a NAT64 prefix so IPv6-only hosts can reach
IPv4-only services via a NAT64 gateway.

## Config
```
acl v6only-clients { 2001:db8:100::/48; };
options {
    dns64 64:ff9b::/96 {
        clients { v6only-clients; };
        mapped { !10.0.0.0/8; !172.16.0.0/12; !192.168.0.0/16; any; };   // do not synthesise for private IPv4
        exclude { 64:ff9b::/96; ::ffff:0:0/96; };                       // ignore bogus real AAAAs
        suffix ::;
        recursive-only yes;
        break-dnssec no;
    };
};
```
- `64:ff9b::/96` is the RFC 6052 well-known prefix; the ARM example uses `mapped { !rfc1918; any; }` to skip private IPv4. If NAT64 must reach private IPv4, use your own prefix (valid lengths are 32, 40, 48, 56, 64 and 96, with bits 64..71 zero) and check RFC 6052 for the well-known prefix limits.
- `exclude` lists AAAA addresses that are ignored when they appear in a name's AAAA records, so DNS64 is applied to its A records instead (default `::ffff:0.0.0.0/96`). `clients` and `mapped` default to `any;`, `suffix` to `::`, `recursive-only` and `break-dnssec` to `no`.
- The NAT64 gateway (Jool, Tayga, router feature) must use the same prefix.

## DNSSEC
Synthesised AAAAs are unsigned. With `break-dnssec no` (the default), when the query has the DO bit set and the applicable records have RRSIGs, synthesis does not happen; `break-dnssec yes` synthesises even if the result would fail validation.

## Test
```
dig @resolver ipv4only.arpa AAAA        # RFC 7050 prefix discovery: answers are synthesised from 192.0.0.170/171
dig @resolver example.org AAAA          # IPv4-only site gets 64:ff9b::<ipv4>
ping6 64:ff9b::8.8.8.8
```

## Gotchas
- DNS64 only affects DNS answers; applications that use IPv4 literals never query it.
- Use `clients { ... }` to limit synthesis to the IPv6-only client networks.
- `dns64` also creates the automatic `ipv4only.arpa` zones unless `ipv4only-enable no;`; `resolver-use-dns64 yes;` lets the server itself reach IPv4-only servers through NAT64.

## Verify
- [ ] An IPv6-only client resolves an IPv4-only site to the NAT64 prefix and connects through the gateway.

## Checked

Date: 2026-10-26. BIND 9 ARM sources in isc-projects/bind9 (main, 9.21 development line, latest tag v9.21.27, plus the bind-9.20 branch grammar), read on 2026-10-26. Confirmed against reference.rst: dns64 prefix lengths, clients/mapped/exclude/suffix/recursive-only/break-dnssec semantics and defaults, example ACL, resolver-use-dns64, ipv4only-enable.

Method: documentation only; no commands were run.
