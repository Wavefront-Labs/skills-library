---
id: computing-software.systems-network-administration.headscale.reverse-proxy-nginx
name: reverse-proxy-nginx
category: computing-software
field: systems-network-administration
product: headscale
tags: [headscale, nginx, connection-upgrade, proxy-buffering, generate-204]
level: advanced
status: docs-checked
description: "Nginx config for proxying Headscale: upstream, Upgrade map, port 80 redirect with generate_204, and TLS server block with True-Client-IP headers."
sources:
  - https://raw.githubusercontent.com/juanfont/headscale/main/docs/ref/integration/reverse-proxy.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Nginx in front of Headscale

Assumes the base configuration from reverse-proxy-requirements (Headscale on `127.0.0.1:8080`).

```nginx
upstream headscale {
    zone upstreams 64K;
    server 127.0.0.1:8080 max_fails=1 fail_timeout=5s;
    keepalive 2;
}

map $http_upgrade $connection_upgrade {
    default keep-alive;
    '' close;
}

server {
    listen 80;
    listen [::]:80;
    server_name <SERVER_NAME>;
    location = /generate_204 { return 204; }
    location / { return 301 https://$server_name$request_uri; }
}

server {
    listen 443 ssl;
    listen [::]:443 ssl;
    http2 on;
    server_name <SERVER_NAME>;
    ssl_certificate <PATH_TO_TLS_CERT>;
    ssl_certificate_key <PATH_TO_TLS_KEY>;
    location / {
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection $connection_upgrade;
        proxy_set_header Host $host;
        proxy_set_header True-Client-IP $remote_addr;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_buffering off;
        proxy_pass http://headscale;
    }
}
```

## Gotchas

- `/generate_204` returning 204 on port 80 supports Tailscale captive portal detection.
- The proxy must support WebSockets for the Tailscale control protocol; this config passes `Upgrade` and `Connection` through.
- Headscale must list the proxy in `trusted_proxies` to honour the IP headers.

## Checked

2026-11-04. Confirmed against the Headscale reverse-proxy page (community documentation, which warns it may be outdated): the Nginx block matches the page, and so do the generate_204 and trusted_proxies remarks.
Method: documentation only; no commands were run.
