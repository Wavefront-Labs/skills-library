---
id: computing-software.networking-hardware-and-wireless.f5-big-ip.dns-wide-ips-and-pools
name: dns-wide-ips-and-pools
category: computing-software
field: networking-hardware-and-wireless
product: f5-big-ip
tags: [networking-hardware-and-wireless, f5-big-ip, wide-ip, gtm-pool, gslb-server]
level: practitioner
status: draft
description: "Configure BIG-IP DNS: data centers, servers, GTM pools and wide IPs with tmsh."
sources:
  - https://techdocs.f5.com/en-us/bigip-15-1-0/big-ip-dns-services-implementations.html
  - https://my.f5.com/manage/s/article/K13823
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# DNS wide IPs, GTM pools and servers

```
tmsh create gtm datacenter dc_east
tmsh create gtm server srv_east datacenter dc_east product bigip addresses add { 10.1.10.245 { device-name bigip1 } } virtual-server-discovery enabled
tmsh create gtm pool a pool_www_east members add { srv_east:vs_web } load-balancing-mode round-robin
tmsh create gtm wideip a www.example.com pools add { pool_www_east } pool-lb-mode global-availability
tmsh show gtm wideip a www.example.com
```
- Hierarchy: data center -> server (BIG-IP or generic host) -> virtual server -> GTM pool (members are server:virtual) -> wide IP (the FQDN, which holds a pool list).
- The wide IP name must match the query name exactly (wildcards allowed: `*.example.com`); the type (`a`, `aaaa`, `cname`, `mx`, `naptr`, `srv`) selects the record type returned. Aliases add alternative names.
- `pool-lb-mode`: `round-robin`, `ratio`, `topology` and `global-availability`. Each pool also has `preferred`, `alternate` and `fallback` load balancing methods, and `fallback-ip` for the last resort.
- Servers of `product bigip` auto-discover virtual servers from LTM; generic hosts need manual virtual servers and a monitor.
- Gotcha: if every pool is unavailable, the answer follows the `fallback-ip`/`return-code` (`ldns` default behaviour); check "Last resort" before blaming the client.

Verify: `dig @listener www.example.com A +short`, and `tmsh show gtm wideip a www.example.com` shows requests, resolutions and `Availability`.
