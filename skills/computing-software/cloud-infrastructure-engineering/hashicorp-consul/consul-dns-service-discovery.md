---
id: computing-software.cloud-infrastructure-engineering.hashicorp-consul.consul-dns-service-discovery
name: consul-dns-service-discovery
category: computing-software
field: cloud-infrastructure-engineering
product: hashicorp-consul
tags: [consul, dns-interface, consul-dns, port-8600]
level: practitioner
status: docs-checked
description: "Query service and node names via Consul DNS on port 8600, understand case sensitivity, and forward the consul domain from the resolver."
sources: ["https://developer.hashicorp.com/consul/docs/services/discovery/dns-overview"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Consul serves DNS on port 8600 by default. Service lookups use `<service>.service.consul`, optionally `<tag>.<service>.service.consul`, and node lookups use `<node>.node.consul`.

```sh
dig @127.0.0.1 -p 8600 web.service.consul SRV
dig @127.0.0.1 -p 8600 v2.web.service.consul
```

To use it from applications, forward all queries for the `consul.` domain from your existing DNS server to a Consul agent rather than changing every app. Service lookups exclude instances whose checks are critical.

Gotchas: all queries are case-sensitive. By default every DNS TTL is 0 (no caching); higher `dns_config.service_ttl` and `node_ttl` values reduce lookups on the servers at the cost of staler results. A UDP query returning more than 3 records sets the truncated flag only when `dns_config.enable_truncate` is true, so clients can retry over TCP; `a_record_limit` caps A, AAAA and ANY answers and does not apply to SRV records. Stale reads (`dns_config.allow_stale`) are enabled by default.

Verify: the `dig` returns A or SRV records for instances that are not critical. Set `dns_config.only_passing = true` to also exclude instances in the warning state.

## Checked

2026-11-03. Confirmed against the Consul DNS reference and configuration pages (port 8600 and consul domain, query syntax, forwarding the consul. domain, default zero TTLs, service_ttl and node_ttl, allow_stale default) and the DNS agent options page (enable_truncate, a_record_limit, only_passing), plus the DNS overview (queries are case-sensitive). Removed: named resolver products, the getent check and the few-seconds TTL advice, which the pages do not state.

Method: documentation only; no commands were run.
