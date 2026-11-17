---
id: computing-software.collaboration-platform-administration.vikunja.reverse-proxy-nginx-apache
name: reverse-proxy-nginx-apache
category: computing-software
field: collaboration-platform-administration
product: vikunja
tags: [vikunja, nginx-proxy-pass, client-max-body-size, apache-proxypass, nginx-proxy-manager]
level: practitioner
status: docs-checked
description: "Reverse-proxy Vikunja with NGINX, NGINX Proxy Manager, Apache or Caddy on port 3456, including the upload size limit and the public URL setting."
sources:
  - https://raw.githubusercontent.com/go-vikunja/website/main/src/content/docs/setup/reverse-proxies.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
All examples assume Vikunja listens on `3456`.

NGINX: in `location /`, `proxy_pass http://localhost:3456;` and `client_max_body_size 20M;`. If you change Vikunja's maximum upload size, change `client_max_body_size` to match.

NGINX Proxy Manager: set `VIKUNJA_SERVICE_PUBLICURL` in compose to the `https://` domain with a trailing slash, expose a host port, add a DNS `A` record to the server IP, then create a Proxy Host with scheme `http`, the server IP, forward port `3456`, Block Common Exploits and Websockets Support toggled. On the SSL tab the docs toggle Force SSL, HTTP/2 and HSTS.

Apache: in `/etc/apache2/sites-available/vikunja.conf` use `ProxyPass / http://localhost:3456/` and `ProxyPassReverse / http://localhost:3456/`, with `<Proxy *>` containing `Require all granted`. Enable modules `proxy`, `proxy_http` and `rewrite`.

Caddy: `reverse_proxy 127.0.0.1:3456` inside a site block for your domain.

The page says to see its client IP section so Vikunja logs and rate limits the real client instead of the proxy (see the client-ip skill).

## Checked

2026-11-04: NGINX, NGINX Proxy Manager, Apache and Caddy settings checked against the reverse proxies page.

Method: documentation only; no commands were run.
