---
id: computing-software.data-engineering.apache-nifi.reverse-proxy-settings
name: reverse-proxy-settings
category: computing-software
field: data-engineering
product: apache-nifi
tags: [data-engineering, apache-nifi, reverse-proxy, nifi-web-proxy-host, context-path, nginx]
level: advanced
status: docs-checked
description: "Running NiFi behind a proxy: nifi.web.proxy.host and nifi.web.proxy.context.path allow lists, and Site-to-Site route properties for proxied clusters."
sources:
  - https://nifi.apache.org/docs/nifi-docs/html/administration-guide.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# NiFi behind a reverse proxy

- `nifi.web.proxy.host`: comma-separated allowed Host header values, for example `localhost:18443, proxyhost:443`. Blank means only the bound host:port is accepted.
- `nifi.web.proxy.context.path`: comma-separated allowed context paths. Blank means any request carrying a proxy context path is rejected.
- Site-to-Site through a proxy uses `nifi.remote.route.{protocol}.{name}.*` with per-route `hostname`, `port` and `secure` (examples in the guide use Nginx).
- Related: `nifi.web.https.application.protocols` defaults to `http/1.1`.

Verify: the UI loads via the proxy URL; if requests are rejected, check that the Host header and any context path are listed in the two allow lists above.

## Checked

Checked against the NiFi Administration Guide, web and Site-to-Site routing properties: `nifi.web.proxy.host` and `nifi.web.proxy.context.path` semantics (including the accepted header names X-ProxyContextPath, X-Forwarded-Context, X-Forwarded-Prefix), the route property set and its `secure` default, and the `http/1.1` default of `nifi.web.https.application.protocols` match. Removed the unsourced log wording from the verify step.

Method: docs-only read of cited pages, 2026-11-08
