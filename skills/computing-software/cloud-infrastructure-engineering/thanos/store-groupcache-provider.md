---
id: computing-software.cloud-infrastructure-engineering.thanos.store-groupcache-provider
name: store-groupcache-provider
category: computing-software
field: cloud-infrastructure-engineering
product: thanos
tags: [thanos-store, groupcache, experimental, caching-bucket]
level: sme
status: docs-checked
description: "Run the experimental groupcache caching-bucket backend across Thanos Store peers, including its security warning."
sources: ["https://thanos.io/tip/components/store.md/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Experimental groupcache caching bucket

Groupcache, available from Thanos v0.25, shares the caching layer between all Thanos Store processes with no external cache. It is a cache-filling library: given enough memory, a value is loaded from object storage once even if several concurrent queries need it.

```yaml
type: GROUPCACHE
config:
  self_url: http://10.123.22.3:8080
  peers:
    - http://10.123.22.3:8080
    - http://10.123.22.10:8080
  groupcache_group: test_group
  dns_interval: 1s
  timeout: 2s
```

- `self_url`: this node's own URL, reachable by the others; it differs per node.
- `groupcache_group`: the group name; every node on the same object storage must use the same name, or they cannot load from each other.
- `peers`: may use a DNS prefix form such as `dns+http://store.thanos.consul.svc:8080`. No trailing slash; one entry must be identical to `self_url`.
- `timeout`: zero means the fetch lives as long as the original request. The docs recommend keeping it above zero.

**Security.** Enabling groupcache registers routes under `/_groupcache`, which let anyone read any data in the configured object storage. If the store is internet-exposed, put a reverse proxy in front and block `/_groupcache/...`.

TLS is supported but the client does not verify the received certificate; HTTP/2 over cleartext is also enabled.

## Checked

2026-11-03. Confirmed against the Thanos Store page (components/store.md): disk sizing (6 MB, 30MB), probes, index cache types and config, memcached and redis options, circuit breaker, caching bucket options, groupcache (v0.25, /_groupcache warning), hedging defaults, request limits and deprecations, time partitioning. Removed the claim about raw Prometheus blocks in the data dir. Removed: closing 'Verify' tips and other statements the page does not state.

Method: documentation only; no commands were run.
