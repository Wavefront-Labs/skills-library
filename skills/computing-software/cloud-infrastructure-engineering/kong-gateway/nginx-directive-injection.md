---
id: computing-software.cloud-infrastructure-engineering.kong-gateway.nginx-directive-injection
name: nginx-directive-injection
category: computing-software
field: cloud-infrastructure-engineering
product: kong-gateway
tags: [kong-gateway, kong, nginx-directives, nginx-http, nginx-proxy, kong-conf, namespaces]
level: practitioner
status: docs-checked
description: "Inject Nginx directives into Kong via nginx_<namespace>_<directive> in kong.conf or KONG_ env vars, with the namespace list (main, events, http, proxy, admin, stream)."
sources:
  - https://developer.konghq.com/gateway/configuration/
  - https://developer.konghq.com/gateway/nginx-directives/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Injecting Nginx directives

Any `kong.conf` property named `nginx_<namespace>_<directive>` is written into the matching Nginx block as `<directive>`.

Namespaces:
- `nginx_main_`: main context
- `nginx_events_`: `events {}`
- `nginx_http_`: `http {}`
- `nginx_proxy_`: proxy `server {}`
- `nginx_location_`: proxy `/` location
- `nginx_upstream_`: proxy `upstream {}`
- `nginx_admin_`: Admin API `server {}`
- `nginx_status_`, `nginx_debug_`: Status and Debug API `server {}`
- `nginx_stream_`, `nginx_sproxy_`, `nginx_supstream_`: stream blocks

Examples from the docs:

```
nginx_proxy_large_client_header_buffers = 16 128k
```
produces `large_client_header_buffers 16 128k;` in the proxy server block.

Environment form: uppercase the property and add `KONG_`, so `KONG_NGINX_HTTP_OUTPUT_BUFFERS="4 64k"` produces `output_buffers 4 64k;` in the `http` block. Likewise `KONG_NGINX_HTTP_SSL_PROTOCOLS` maps to `nginx_http_ssl_protocols`.

Proxy and Admin API TLS versions can differ: `nginx_proxy_ssl_protocols` and `nginx_admin_ssl_protocols` take precedence over the `http {}` value.

## Checked

2026-11-04. Confirmed against kong.conf.default (full namespace list, `KONG_` form, `ssl_protocols` precedence note) and the Nginx directives page (the large_client_header_buffers and output_buffers examples). Nothing removed.
Method: documentation only; no commands were run.
