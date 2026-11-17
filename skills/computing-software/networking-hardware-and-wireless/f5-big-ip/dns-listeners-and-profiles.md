---
id: computing-software.networking-hardware-and-wireless.f5-big-ip.dns-listeners-and-profiles
name: dns-listeners-and-profiles
category: computing-software
field: networking-hardware-and-wireless
product: f5-big-ip
tags: [networking-hardware-and-wireless, f5-big-ip, dns-listener, dns-profile, dns-cache]
level: practitioner
status: draft
description: "Create BIG-IP DNS listeners, assign DNS profiles (GSLB, cache, DNSSEC) and avoid open resolver exposure."
sources:
  - https://techdocs.f5.com/en-us/bigip-15-1-0/big-ip-dns-services-implementations.html
  - https://www.f5.com/pdf/certification/exams/blueprint-tmos-administration.pdf
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# DNS listeners, DNS profiles and caching

```
tmsh create gtm listener ls_53_udp address 10.1.10.53 port 53 ip-protocol udp profiles add { dns }
tmsh create gtm listener ls_53_tcp address 10.1.10.53 port 53 ip-protocol tcp profiles add { dns }
tmsh create ltm profile dns dns_gslb defaults-from dns enable-gtm yes use-local-bind no enable-dnssec no
tmsh create ltm dns cache transparent cache_rr
tmsh modify gtm listener ls_53_udp profiles replace-all-with { dns_gslb }
```
- A listener is a virtual server on port 53 for BIG-IP DNS that answers wide IP queries. Create both UDP and TCP (TCP is needed for truncation and large DNSSEC answers).
- Profile options: `enable-gtm` (answer wide IPs), `use-local-bind` (forward to local BIND zone files), `enable-dns-express` (zone serving), `enable-dnssec`, `enable-cache` with a `cache` object (resolver, transparent or validating).
- Resolver caches on the Internet-facing listener make an open recursive resolver. Restrict via `allow-service`, source IP VLAN limits, or answer only authoritative zones.
- Gotcha: a listener address that equals a self IP address conflicts; use a distinct virtual address, or a wildcard listener with `0.0.0.0` and packet filtering.
- Add DNS request/response logging via `dns logging profile` only when required; high QPS fills disks.

Verify: `dig @10.1.10.53 www.example.com +tcp` and `+udp`; `tmsh show ltm profile dns dns_gslb` shows queries and responses; `tcpdump -nni 0.0 port 53`.
