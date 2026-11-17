---
id: computing-software.cybersecurity-defensive.authentik.reverse-proxy-setup
name: reverse-proxy-setup
category: computing-software
field: cybersecurity-defensive
product: authentik
tags: [authentik, reverse-proxy, nginx, traefik, trusted-proxy-cidrs, forwarded-headers]
level: practitioner
status: docs-checked
description: "Put authentik behind nginx or Traefik: required forwarded headers, WebSocket upgrade, AUTHENTIK_LISTEN__TRUSTED_PROXY_CIDRS and fixing mixed-content or wrong client IP symptoms."
sources:
  - https://docs.goauthentik.io/install-config/reverse-proxy/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: expose authentik through a proxy without breaking outposts, redirects or client IPs. The proxy must speak HTTP/1.1 or newer (outposts use WebSockets).

## Headers the proxy must set (overwriting client-supplied values)
`X-Forwarded-Host` or `Host`, `X-Forwarded-Proto`, `X-Forwarded-For`, and `Connection: Upgrade` plus `Upgrade: WebSocket`.

## Trusted proxy networks
authentik only honours these headers (except Connection and Upgrade) from trusted networks. Default list: `127.0.0.0/8`, `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`, `fe80::/10`, `::1/128`. Setting `AUTHENTIK_LISTEN__TRUSTED_PROXY_CIDRS` replaces that list, so include every address a proxy connects from, and never networks from which untrusted clients reach authentik directly. Helm: `authentik.listen.trusted_proxy_cidrs`.

## nginx
Upstream `server <host>:9443;` (or 9000 with `proxy_pass http://authentik;`), then in `location /`:
```nginx
proxy_pass https://authentik;
proxy_http_version 1.1;
proxy_set_header X-Forwarded-Proto $scheme;
proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
proxy_set_header Host $http_host;
proxy_set_header Upgrade $http_upgrade;
proxy_set_header Connection $connection_upgrade_keepalive;
```
with `map $http_upgrade $connection_upgrade_keepalive { default upgrade; '' ''; }`.

## Traefik (Docker labels on the `server` service)
`traefik.http.routers.authentik.rule: "Host(`sso.domain.tld`)"`, `...entrypoints: websecure`, `...service: authentik`, `traefik.http.services.authentik.loadbalancer.server.port: "9000"`. For port 9443 also set `...server.scheme: https` and a ServersTransport with `serverName`; the default self-signed certificate will not verify. Do not apply authentik forward-auth middleware to authentik's own router (redirect loop).

## Symptoms
Endless spinner or mixed-content error: proxy not sending `X-Forwarded-Proto: https` or its source is untrusted. Wrong client IPs: proxy outside the CIDR list. Traefik 502: port or scheme mismatch. Do not cache anything but `/static/*`.

## Checked

Method: docs-checked 2026-11-09 against https://docs.goauthentik.io/install-config/reverse-proxy/ (read in full).
