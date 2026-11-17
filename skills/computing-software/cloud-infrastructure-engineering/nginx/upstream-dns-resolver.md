---
id: computing-software.cloud-infrastructure-engineering.nginx.upstream-dns-resolver
name: upstream-dns-resolver
category: computing-software
field: cloud-infrastructure-engineering
product: nginx
tags: [nginx, resolver, dns, dynamic-upstream, valid]
level: practitioner
status: docs-checked
description: "DNS resolution in nginx: resolver with valid=, variables in proxy_pass, and upstream server resolve with a shared-memory zone."
sources: ["https://nginx.org/en/docs/http/ngx_http_core_module.html", "https://nginx.org/en/docs/http/ngx_http_upstream_module.html", "https://nginx.org/en/docs/http/ngx_http_proxy_module.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

```nginx
resolver 10.0.0.2 valid=30s ipv6=off;
resolver_timeout 5s;

location / {
    set $backend "http://api.internal.example.com";
    proxy_pass $backend;
}
```

- `resolver address ... [valid=time] [ipv4=on|off] [ipv6=on|off]` (contexts `http`, `server`, `location`): name servers are queried round-robin, the default port is 53, and nginx looks up both IPv4 and IPv6 unless `ipv4=off` / `ipv6=off`. Answers are cached by the response TTL; `valid=` overrides that. The docs recommend a secured trusted local network for DNS servers because of spoofing. `resolver_timeout` defaults to `30s`.
- When `proxy_pass` contains variables and the address is a domain name, nginx first searches the defined server groups for that name and, if not found, resolves it with the `resolver`.
- In an `upstream` block, the `server` parameter `resolve` monitors changes of the IP addresses behind a domain name and updates the upstream without a restart. The group must have a shared-memory `zone`, and a `resolver` must be set in the `http` block or the `upstream` block. Before 1.27.3 this was a commercial-subscription feature. `service=name` with `resolve` enables SRV record lookups.

```nginx
upstream dynamic {
    zone upstream_dynamic 64k;
    resolver 10.0.0.2;           # upstream-level resolver, since 1.27.3
    server backend3.example.com resolve;
}
```

## Checked
Date: 2026-11-03.
Confirmed in the core, proxy and upstream module pages: resolver syntax and parameters, defaults, caching/valid, spoofing note, variable lookup order, `resolve` and `zone` requirements, version note, upstream-level resolver.
Removed as unconfirmed: "resolved once at config load" wording, claims about /etc/hosts, Docker/Kubernetes DNS addresses, the error text, the loss of keepalive and balancing with variables, and the access-log verify step.
Method: documentation only; no commands were run.
