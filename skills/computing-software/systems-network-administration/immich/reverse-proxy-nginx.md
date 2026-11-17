---
id: computing-software.systems-network-administration.immich.reverse-proxy-nginx
name: reverse-proxy-nginx
category: computing-software
field: systems-network-administration
product: immich
tags: [nginx, caddy, apache, reverse-proxy, websockets, uploads]
level: practitioner
status: docs-checked
description: "Front Immich with nginx, Caddy or Apache: required headers, large upload settings, websocket support, timeouts and the root-path limitation."
sources:
  - https://docs.immich.app/administration/reverse-proxy
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: terminate TLS in a custom reverse proxy without breaking uploads or the mobile app.

Rules for any proxy between Immich and users:

- Forward all headers and set `Host`, `X-Real-IP`, `X-Forwarded-Proto` and `X-Forwarded-For` correctly.
- Allow big uploads.
- Serve Immich on the root of a (sub)domain. A sub-path such as `location /immich {` is not supported.
- With a Let's Encrypt http-01 challenge, make sure `/.well-known/immich` still routes to Immich, or the mobile app may fail to connect.

nginx server block essentials (backend listens on port 2283):

```nginx
client_max_body_size 50000M;
proxy_request_buffering off;
client_body_buffer_size 1024k;
proxy_set_header Host              $host;
proxy_set_header X-Real-IP         $remote_addr;
proxy_set_header X-Forwarded-For   $proxy_add_x_forwarded_for;
proxy_set_header X-Forwarded-Proto $scheme;
proxy_http_version 1.1;
proxy_redirect     off;
proxy_read_timeout 600s;
proxy_send_timeout 600s;
send_timeout       600s;
location / {
    proxy_pass http://<backend_url>:2283;
    proxy_set_header Upgrade    $http_upgrade;
    proxy_set_header Connection "upgrade";
}
```

Turning off request buffering avoids out-of-memory on the proxy and makes uploads faster.

Caddy needs only:

```
immich.example.org {
    reverse_proxy http://<backend>:2283
}
```

Apache: use `ProxyPass / http://127.0.0.1:2283/ timeout=600 upgrade=websocket`, `ProxyPassReverse` and `ProxyPreserveHost On`.

## Checked

2026-11-03. Confirmed against the Immich docs (https://docs.immich.app/) by reading: administration/reverse-proxy (intro, Nginx, Caddy, Apache).
Removed or reworded: nothing needed removal.
Method: documentation only; no commands were run.
