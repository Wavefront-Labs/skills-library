---
id: computing-software.systems-network-administration.dns-dhcp.bind-recursion-acl-and-forwarders
name: bind-recursion-acl-and-forwarders
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dns, bind, named-conf, recursive-resolver, dns-resolver, allow-recursion, allow-query-cache, open-resolver, forwarders, forward-only, forward-first, conditional-forwarding, forward-zone, dnssec-validation]
level: practitioner
status: verified
description: "Run BIND as an internal resolver safely: allow-recursion ACLs that prevent an open resolver, global forwarders vs full recursion, forward-only zones for AD/partners, and testing."
sources:
  - https://bind9.readthedocs.io/en/latest/reference.html
  - https://bind9.readthedocs.io/en/latest/manpages.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# BIND recursion ACLs and forwarders

## Never run an open resolver
An open resolver (answers recursive queries from the internet) is abused for DNS amplification
DDoS and cache poisoning attempts.
```
acl internal { 10.0.0.0/8; 172.16.0.0/12; 192.168.0.0/16; 127.0.0.1; ::1; 2001:db8::/32; };
options {
    directory "/var/cache/bind";
    recursion yes;
    allow-recursion { internal; };
    allow-query-cache { internal; };
    allow-query { internal; };          // on a resolver-only box
    dnssec-validation auto;             // enables validation with the built-in root trust anchor
    listen-on { 10.0.0.53; 127.0.0.1; };
    listen-on-v6 { 2001:db8::53; ::1; };
    minimal-responses yes;
};
```
Authoritative servers facing the internet: `recursion no;` (separate roles onto separate servers or
views). Test from outside with a name the server is not authoritative for: `dig @<public-ip> www.isc.org +rec` must return REFUSED (an authoritative server answers names in its own zones with the `aa` flag even with `recursion no`).
If `allow-recursion` is unset, BIND uses `allow-query-cache`, then `allow-query`, and finally the default `localnets; localhost;`.

## Full recursion vs forwarders
- **Full recursion** (default, no forwarders): resolver talks to root/TLD/authoritatives itself;
  independent, DNSSEC-validating, no third party sees all queries.
- **Global forwarders** (to an ISP or a filtering service): needed when policy
  requires filtering or the firewall only allows DNS to specific upstreams.
  ```
  options { forwarders { 192.0.2.10; 192.0.2.11; }; forward only; };
  ```
  `forward only` queries only the forwarders; `forward first` (the default) falls back to resolving
  the name itself if the forwarders do not answer (can leak queries past your filtering provider).

## Conditional forwarding (per zone)
```
zone "corp.example" { type forward; forward only; forwarders { 10.1.1.10; 10.1.1.11; }; };
zone "10.in-addr.arpa" { type forward; forward only; forwarders { 10.1.1.10; 10.1.1.11; }; };
```
Typical for AD-integrated domains and partner zones reachable over VPN. If those zones are unsigned
but under a signed parent, validation can fail: add `validate-except { "corp.example"; };` (a permanent
exemption at and below that name) or use a negative trust anchor (`rndc nta corp.example`, which expires).

## Test
```
named-checkconf && rndc reconfig
dig @10.0.0.53 www.isc.org +dnssec          # 'ad' flag = validated
dig @10.0.0.53 dc01.corp.example
rndc querylog on                            # briefly, then rndc querylog off
```

## Verify
- [ ] External recursive query refused; internal clients resolve internet and corp names.
- [ ] Validation on (`ad` flag) and conditional zones work.

## Checked

Date: 2026-10-26. BIND 9 ARM sources in isc-projects/bind9 (main, 9.21 development line, latest tag v9.21.27, plus bind-9.20 branch notes and grammar), read on 2026-10-26. Confirmed: allow-recursion fallback chain and localnets/localhost default, allow-query-cache defaults, forward first (default) vs only, type forward zones, validate-except semantics versus negative trust anchors, rndc nta and querylog. Removed unconfirmed vendor resolver addresses, the nmap script and version gates.

Method: documentation, plus commands run 2026-11-01 in a Debian 13 (trixie) rootless Podman container (BIND 9.20.30): recursion yes with allow-recursion/allow-query-cache/allow-query ACL (client in the ACL resolved through a forward zone, another source address REFUSED), allow-query-cache alone also gating recursion when allow-recursion is unset, recursion no on an authoritative server (a name in its own zone answered with aa even with +rec), forward only to a dead forwarder SERVFAIL, validate-except parsed by named-checkconf. Corrected the external test: REFUSED applies to names the server is not authoritative for. Not run: forward first fallback, rndc nta, rndc querylog, the localnets default, DNSSEC validation (no root reachable).
