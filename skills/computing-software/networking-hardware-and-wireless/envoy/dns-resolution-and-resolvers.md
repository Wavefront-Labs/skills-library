---
id: computing-software.networking-hardware-and-wireless.envoy.dns-resolution-and-resolvers
name: dns-resolution-and-resolvers
category: computing-software
field: networking-hardware-and-wireless
product: envoy
tags: [networking-hardware-and-wireless, envoy, dns-resolution, c-ares, getaddrinfo, hickory, strict-dns, dns-lookup-family, respect-dns-ttl]
level: practitioner
status: docs-checked
description: "Pick and tune Envoy DNS resolution (c-ares default, getaddrinfo, Hickory) for strict and logical DNS clusters and failure fallback behaviour."
sources:
  - https://github.com/envoyproxy/envoy/blob/main/docs/root/intro/arch_overview/upstream/dns_resolution.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# dns resolution and resolvers
Many Envoy parts resolve DNS: strict and logical DNS clusters, the dynamic forward proxy (cluster plus filter), the UDP DNS filter. Resolution is pluggable. The default is c-ares; Apple platforms can use Apple APIs via the `envoy.restart_features.use_apple_api_for_dns_lookups` runtime feature. The built-in resolver extensions are c-ares, Apple, getaddrinfo and Hickory DNS (a Rust resolver loaded through dynamic modules, supporting UDP/TCP, DoT, DoH and DNSSEC, running on its own Tokio threads so it does not block the dispatcher).

```yaml
clusters:
- name: ext
  type: STRICT_DNS
  respect_dns_ttl: true
  dns_refresh_rate: 5s
  dns_lookup_family: V4_PREFERRED
```
Behaviour notes from the docs:
- With c-ares, `AUTO` and `V4_PREFERRED` try the other address family if the preferred returns nothing; if neither lookup gives addresses and one fails, the resolution fails. Strict DNS clusters keep existing hosts on a failed resolution.
- `respect_dns_ttl` makes record TTL and `dns_refresh_rate` control refresh timing.
- With c-ares, a successful fallback still returns its addresses, and lookups that both report no records return a successful empty result.

Gotcha: the Apple and Hickory resolvers emit stats trees (`dns.apple`, `dns.hickory`) with counters such as `get_addr_failure`. Admin `GET /clusters` lists the hosts a cluster currently has.

## Checked
2026-11-03. Confirmed against dns_resolution.rst and the Cluster reference. Removed or corrected: the 'never resolves DNS synchronously' claim, the zero-address claim and the update_success/update_failure stats.
Method: documentation only; no commands were run.
