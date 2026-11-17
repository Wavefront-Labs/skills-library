---
id: computing-software.systems-network-administration.coredns.coredns-k8s-external
name: coredns-k8s-external
category: computing-software
field: systems-network-administration
product: coredns
tags: [coredns, k8s-external, kubernetes, loadbalancer, external-ip]
level: practitioner
status: docs-checked
description: "Resolve LoadBalancer and external IPs of Kubernetes services, and optionally headless services, from an extra zone with k8s_external."
sources:
  - https://coredns.io/plugins/k8s_external/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: publish in-cluster service addresses under an external zone.

k8s_external only works if the kubernetes plugin is also loaded. It handles A, AAAA, SRV and PTR queries, and SOA and NS at the zone apex. The apex SOA serial is static, and the nameserver records point to the CoreDNS service addresses under the `dns` subdomain.

Syntax:

```
k8s_external [ZONE...] {
    apex APEX
    ttl TTL
    headless
    fallthrough [ZONE...]
}
```

- `apex APEX`: DNS label used for the apex records; default `dns`.
- `ttl TTL`: response TTL; default 5 seconds.
- `headless`: if a headless service has external IPs set, resolve them.
- `fallthrough [ZONE...]`: pass a query for a nonexistent name to the next plugin that matches the zone.

The plugin answers the dns subdomain and the zone apex itself; all other names resolve to addresses in the cluster, for example `service.namespace.example.org`.

Example apex records for zone example.org: `example.org. 5 IN SOA ns1.dns.example.org. hostmaster.example.org. (...)` with refresh 7200, retry 1800, expire 86400 and minimum 5, plus an `example.org. 5 IN NS ns1.dns.example.org.` record and `ns1.dns.example.org.` A and AAAA records holding the CoreDNS service IPs.

Example: `kubernetes cluster.local` and `k8s_external example.org` in one block give a Service `test` in namespace `default` with externalIPs an `A` record for `test.default.example.org`. It can be combined with the transfer plugin (`transfer example.org { to * }`) for zone transfers; NOTIFY is not supported.

## Checked

2026-11-08. Checked in full against the k8s_external plugin README. Corrected the SOA values (refresh 7200, retry 1800, expire 86400, minimum 5, not 14400 and 604800), fixed the headless description, added the fallthrough option and transfer example, removed an unsupported ordering claim.

Method: documentation only; no commands were run.
