---
id: computing-software.devops-ci-cd.verdaccio.nginx-reverse-proxy
name: nginx-reverse-proxy
category: computing-software
field: devops-ci-cd
product: verdaccio
tags: [nginx, reverse-proxy, client-max-body-size, nginx-config, proxy-pass, x-forwarded-proto, http-413]
level: practitioner
status: docs-checked
description: "Put nginx in front of Verdaccio: required forwarded headers, client_max_body_size 0 to avoid 413 on publish, TLS server block and sub-directory locations."
sources:
  - https://verdaccio.org/docs/reverse-proxy/
  - https://verdaccio.org/docs/configuration/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Root install:
```
server {
    listen 80;
    client_max_body_size 0;      # nginx default 1 MB makes big npm publish fail with 413
    location / {
        proxy_pass http://127.0.0.1:4873/;
        proxy_set_header Host $host:$server_port;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }
}
```
Verdaccio resolves its public URL from `X-Forwarded-Proto` and `Host`, so send both. Also set `server.trustProxy` in `config.yaml`.

TLS: `listen 443 ssl;` plus `http2 on;` (the standalone `ssl on;` was removed in nginx 1.25.1 and the `http2` listen parameter is deprecated), `ssl_certificate`, `ssl_certificate_key`, `ssl_protocols TLSv1.2 TLSv1.3;` and `proxy_read_timeout 600;`; redirect port 80 with `return 302 https://$host$request_uri;`.

Sub-directory:
```
location ~ ^/verdaccio/(.*)$ {
    proxy_pass http://127.0.0.1:4873/$1;
    proxy_set_header Host $host:$server_port;
    proxy_set_header X-Forwarded-Proto $scheme;
}
```
with `url_prefix: /verdaccio/` (trailing slash). At the root, do not set `url_prefix`.

## Checked

2026-11-04. Read the Verdaccio documentation pages: Reverse Proxy and Configuration (Running behind a proxy, URL Prefix). Confirmed: client_max_body_size 0 for 413, the forwarded headers, the TLS block with http2 on, the removal of ssl on in nginx 1.25.1, proxy_read_timeout 600, the 302 redirect, the sub-directory block and url_prefix rules, trustProxy. Removed or corrected: the dead url-prefix source (404), replaced by the Configuration page.

Method: documentation only; no commands were run.
