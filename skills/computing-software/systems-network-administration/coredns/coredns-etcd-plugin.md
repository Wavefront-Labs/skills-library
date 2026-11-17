---
id: computing-software.systems-network-administration.coredns.coredns-etcd-plugin
name: coredns-etcd-plugin
category: computing-software
field: systems-network-administration
product: coredns
tags: [coredns, etcd, skydns, service-discovery, backend]
level: advanced
status: docs-checked
description: "Serve SkyDNS-style records from etcd, with path, endpoint, credentials, TLS, lease TTL options and its subtree lookup behaviour."
sources:
  - https://coredns.io/plugins/etcd/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: use etcd as a DNS backend.

The plugin implements the older SkyDNS format; data must be encoded as a SkyDNS message. It is not a generic zone data plugin: only a subset of record types is supported, and subdomains and delegations are not handled.

Syntax:

```
etcd [ZONES...] {
    fallthrough [ZONES...]
    path PATH
    endpoint ENDPOINT...
    credentials USERNAME PASSWORD
    tls CERT KEY CACERT
}
```

Defaults: path `/skydns`, endpoint `http://localhost:2379` (etcd3). `min-lease-ttl` defaults to 30 seconds and `max-lease-ttl` to 24 hours, bounding TTLs derived from etcd lease duration.

Behaviour: the plugin searches the entire subtree and returns all records found, so a query for `mx.skydns.test` returns entries `a` and `b` under `/skydns/test/skydns/mx`. With etcd3 keys are flat, so it looks up the prefix with a trailing slash and, if nothing is found, the bare key, which causes two etcd lookups in some cases.

Examples:
- Reverse zones: add `0.0.10.in-addr.arpa` (or `10.0.0.0/24`) to the zones and `etcdctl put /skydns/arpa/in-addr/10/0/0/127 '{"host":"reverse.skydns.local."}'`.
- A zone-name record: `etcdctl put /skydns/local/skydns/ '{"host":"1.1.1.1","ttl":60}'`.
- SRV: JSON includes `priority` and `port`; TXT uses `text`.

For round-robin of A and AAAA see loadbalance.

## Checked

2026-11-03. Page read: https://coredns.io/plugins/etcd/ (the CoreDNS plugin page).

Confirmed: the syntax, options, defaults, limits, metric names and examples stated in this skill.

Removed or corrected: nothing.

Method: documentation only; no commands were run.
