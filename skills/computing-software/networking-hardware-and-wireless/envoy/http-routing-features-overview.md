---
id: computing-software.networking-hardware-and-wireless.envoy.http-routing-features-overview
name: http-routing-features-overview
category: computing-software
field: networking-hardware-and-wireless
product: envoy
tags: [networking-hardware-and-wireless, envoy, router, http-routing, virtual-hosts, prefix-rewrite, redirect, timeouts, hedging]
level: practitioner
status: docs-checked
description: "List what the Envoy HTTP router filter can do (virtual hosts, matching, rewrites, redirects, retries, timeouts) and where each is configured."
sources:
  - https://github.com/envoyproxy/envoy/blob/main/docs/root/intro/arch_overview/http/http_routing.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# http routing features overview
The router filter (`envoy.filters.http.router`) must be the last HTTP filter. It matches a request to a route, picks an upstream cluster, acquires a connection pool to a host and forwards the request. It serves edge reverse-proxy duty, service-to-service meshes (routing on Host/authority) and forward-proxy setups.

Capabilities listed in the docs:
- Virtual hosts map domains to routes; a virtual cluster (regex matchable) yields extra stats on top of cluster stats.
- Matching on case-sensitive or insensitive prefix, exact path, `safe_regex`, arbitrary headers, and cookies.
- Rewriting: `prefix_rewrite`, `regex_rewrite` with capture groups, explicit host rewrite and `auto_host_rewrite` from the chosen upstream DNS name.
- Redirects: `path_redirect` / `host_redirect` per route, `require_tls` per virtual host.
- Request timeouts, retries and hedging.

```yaml
route_config:
  virtual_hosts:
  - name: svc
    domains: ["svc.example.com"]
    routes:
    - match: { prefix: "/api/" }
      route: { cluster: api, prefix_rewrite: "/", timeout: 5s }
```
Gotcha: routes are evaluated in order and the first match wins, so put specific prefixes before `/`. Verify with `GET /config_dump` on the admin port.

## Checked

2026-11-03. Confirmed against: http_routing.rst (router last, virtual hosts, matching, rewrites, redirects, retries, hedging) and admin.rst (/config_dump). Removed or corrected: the router check tool reference.

Method: documentation only; no commands were run.
