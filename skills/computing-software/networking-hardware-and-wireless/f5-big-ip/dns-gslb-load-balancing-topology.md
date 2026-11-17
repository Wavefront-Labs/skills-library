---
id: computing-software.networking-hardware-and-wireless.f5-big-ip.dns-gslb-load-balancing-topology
name: dns-gslb-load-balancing-topology
category: computing-software
field: networking-hardware-and-wireless
product: f5-big-ip
tags: [networking-hardware-and-wireless, f5-big-ip, gslb-topology, topology-records, dns-persistence]
level: practitioner
status: draft
description: "Configure BIG-IP DNS topology regions and records, ratio methods, and persistence so users resolve to the nearest healthy data center."
sources:
  - https://techdocs.f5.com/en-us/bigip-15-1-0/big-ip-dns-services-implementations.html
  - https://my.f5.com/manage/s/article/K13823
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# GSLB load balancing methods, topology and persistence

```
tmsh create gtm region eu_users members add { country DE country FR subnet 198.51.100.0/24 }
tmsh create gtm topology ldns: region eu_users server: datacenter dc_eu score 100
tmsh create gtm topology ldns: subnet 0.0.0.0/0 server: datacenter dc_us score 10
tmsh modify gtm pool a pool_www preferred-lb-mode topology alternate-lb-mode round-robin fallback-lb-mode return-to-dns
tmsh modify gtm wideip a www.example.com persistence enabled persist-cidr-ipv4 24 ttl-persistence 3600
```
- Topology matches the LDNS (recursive resolver) address, not the user. Records are scored: the highest score wins, and region (continent/country/state, from the geolocation DB) or subnet or data center or pool can be matched.
- Methods: `round-robin`, `ratio`, `global-availability`, `topology`, `qos`, `completion-rate`, `round-trip-time`, `kilobytes-per-second`, `packet-rate` and `static-persist`. Dynamic methods need probing (LDNS paths) from the BIG-IP DNS.
- Order is preferred, then alternate, then fallback; `return-to-dns` hands the query to the local BIND or returns SERVFAIL (depending on the `fallback-ip`), so choose deliberately.
- GeoIP data needs regular updates (`geoip-update` / the F5 location database RPM); stale data misroutes new IP ranges.
- Gotcha: DNS persistence requires a TTL long enough to matter and caches/LDNS ignore short TTLs differently; set `ttl` on the pool.

Verify: `dig @listener www.example.com +subnet=198.51.100.5/32` (EDNS client-subnet) from a test box; `tmsh show gtm topology` and `tmsh show gtm wideip a www.example.com` for hit counters.
