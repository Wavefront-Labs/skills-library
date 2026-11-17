---
id: computing-software.systems-network-administration.uptime-kuma.uptime-kuma-reverse-proxy-websocket-headers
name: uptime-kuma-reverse-proxy-websocket-headers
category: computing-software
field: systems-network-administration
product: uptime-kuma
tags: [reverse-proxy, websocket, nginx, apache, trust-proxy, x-forwarded-for, nginx-proxy-manager]
level: practitioner
status: docs-checked
description: "Put Uptime Kuma behind nginx or Apache with the WebSocket Upgrade and Connection headers and trusted proxy settings."
sources: ["https://github.com/louislam/uptime-kuma/wiki/Reverse-Proxy"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Reverse proxy for Uptime Kuma

Uptime Kuma uses WebSocket, so the proxy must pass the `Upgrade` and `Connection` headers. Subdirectories such as `/uptimekuma` are not supported: use a domain or subdomain.

nginx:

```nginx
server {
  listen 443 ssl http2;
  server_name sub.domain.com;
  ssl_certificate     /path/to/ssl/cert/crt;
  ssl_certificate_key /path/to/ssl/key/key;
  location / {
    proxy_set_header   X-Real-IP $remote_addr;
    proxy_set_header   X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header   Host $host;
    proxy_pass         http://localhost:3001/;
    proxy_http_version 1.1;
    proxy_set_header   Upgrade $http_upgrade;
    proxy_set_header   Connection "upgrade";
  }
}
```

Apache needs `ProxyPreserveHost on`, `ProxyPass / http://localhost:3001/`, and a RewriteRule sending requests with `Upgrade: websocket` to `ws://localhost:3001/$1`. Nginx Proxy Manager: enable WebSockets Support. Caddy obtains certificates automatically; for nginx or Apache the page recommends Certbot.

If Uptime Kuma is reachable only through the proxy (firewall enforced), go to Settings, Reverse Proxy, HTTP Headers and set Trust Proxy to Yes so `X-Forwarded-*` headers give the right client IP in logs.

Related: for status pages on custom domains the proxy must forward `X-Forwarded-Host` or `Host` (see uptime-kuma-status-pages-and-custom-domains).

## Checked

2026-11-04. Confirmed against the Uptime Kuma wiki: Reverse Proxy page (WebSocket headers, subdirectory note, nginx and Apache configs, Nginx Proxy Manager, Certbot, Trust Proxy) and Status Page page (X-Forwarded-Host). Removed: The claim that clients could spoof headers when Trust Proxy is on, and the generic verify line.

Method: documentation only; no commands were run.
