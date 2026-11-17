---
id: computing-software.cybersecurity-defensive.zitadel.reverse-proxy-and-login-ui-routing
name: reverse-proxy-and-login-ui-routing
category: computing-software
field: cybersecurity-defensive
product: zitadel
tags: [zitadel, reverse-proxy, traefik, nginx, caddy, login-v2]
level: advanced
status: docs-checked
description: "Put a reverse proxy in front of ZITADEL with h2c upstream, correct host handling and path routing between the API and the Login V2 UI."
sources:
  - https://zitadel.com/docs/self-hosting/manage/reverseproxy/reverse_proxy
  - https://zitadel.com/docs/self-hosting/manage/requirements
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
ZITADEL exposes one HTTP/2 port, default 8080, serving gRPC, REST APIs and the console. A reverse proxy in front is recommended for production because it terminates TLS, exposes standard ports 80 and 443, handles certificate renewal such as Let's Encrypt, and routes by path between the API and the Login UI.

Requirements:

- When the proxy terminates TLS it must forward to ZITADEL with h2c, not HTTP/1.1.
- Use the `external` TLS mode for a proxy that terminates TLS, and `enabled` where you need end-to-end encryption.
- Tested proxies with dedicated guides: Traefik v3.x, NGINX v1.x stable, Caddy v2.x and Apache httpd 2.4.x. Cloudflare, Cloudflare Tunnel and fronting ZITADEL Cloud guides also exist.

Login V2 routing: send `/ui/v2/login` to the Login UI container, port 3000 by default, and every other path to the ZITADEL API container, port 8080 by default.

Any proxy that supports HTTP/2 upstream connections (h2c or h2) works; the four named above are the tested ones.

## Checked

2026-11-08. Read in full: the reverse proxy page and the requirements page. Removed the line about forwarding the original Host and the pre-go-live test advice, which neither page states.

Method: documentation only; no commands were run.
