---
id: computing-software.cloud-infrastructure-engineering.nginx.load-balancing-methods
name: load-balancing-methods
category: computing-software
field: cloud-infrastructure-engineering
product: nginx
tags: [nginx, least-conn, load-balancing, round-robin, ip-hash, random, least-time]
level: practitioner
status: docs-checked
description: "Choosing among round robin, least_conn, ip_hash, hash, random two and least_time in nginx upstream groups, and the zone directive."
sources: ["https://nginx.org/en/docs/http/ngx_http_upstream_module.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Without a method directive an `upstream` group uses weighted round robin (`weight=number` on `server`, default 1). If an error occurs communicating with a server, the request goes to the next one until all working servers are tried.

```nginx
upstream app {
    least_conn;
    server a:8080 weight=2;
    server b:8080;
}
upstream hashed { ip_hash; server a:80; server b:80; }
upstream rnd    { random two least_conn; server a:80; server b:80; server c:80; }
```

- `least_conn;` sends the request to the server with the fewest active connections, taking weights into account; ties use weighted round robin.
- `ip_hash;` hashes the first three octets of an IPv4 client address (whole IPv6 address); mark a server `down` instead of removing it to preserve the mapping.
- `hash key [consistent];` hashes an arbitrary key (see the hash skill).
- `random [two [method]];` (1.15.1) picks a server at random, weight-aware. With `two` it picks two at random and chooses between them with the method; the default method is `least_conn`.
- `least_time header | last_byte [inflight];` picks the server with the lowest average response time and fewest active connections. Before 1.31.0 it was available only as part of the commercial subscription. `random two least_time=header` or `least_time=last_byte` is also accepted, with the same availability note.
- `zone name [size];` (1.9.0) puts the group's configuration and run-time state in shared memory shared between worker processes.

## Checked

2026-11-03. Confirmed against the nginx `ngx_http_upstream_module` page. Removed: workload guidance (which method suits uploads or fleets of nginx instances), the NAT/CDN and "not true affinity" commentary, per-worker counter claim, the `add_header X-Upstream` Verify step, and the confirm marker on `least_time` (now stated from the page).
Method: documentation only; no commands were run.
