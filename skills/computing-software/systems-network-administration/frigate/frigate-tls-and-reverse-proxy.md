---
id: computing-software.systems-network-administration.frigate.frigate-tls-and-reverse-proxy
name: frigate-tls-and-reverse-proxy
category: computing-software
field: systems-network-administration
product: frigate
tags: [tls-certificates, self-signed-certificate, reverse-proxy, websocket-support, disable-tls, certbot-symlinks]
level: practitioner
status: docs-checked
description: "Control Frigate's TLS on port 8971, mount your own certificates and configure a reverse proxy with WebSocket support."
sources: ["https://docs.frigate.video/configuration/tls/", "https://docs.frigate.video/guides/reverse_proxy/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# TLS and reverse proxy for Frigate

By default Frigate's NGINX generates a self-signed certificate for port 8971, stored in `/config/tls` so it survives container recreation. If a reverse proxy terminates TLS, disable it with `tls.enabled: False`; otherwise plain HTTP to the TLS port causes an HTTP 400 error ("The plain HTTP request was sent to HTTPS port").

Own certificates: mount a folder at `/etc/letsencrypt/live/frigate` containing `privkey.pem` and `fullchain.pem`; mounted files take precedence over the self-signed pair. `privkey.pem` must be readable by the runtime user running NGINX. Frigate adjusts ownership at start when the mount is writable, but on a `:ro` mount you must make it readable by uid 1000 (or your `PUID`). Certbot uses symlinks, so also mount the matching `archive` folder (for example `/etc/letsencrypt/archive/your.fqdn.net`) or the links will not resolve.

Reverse proxy: check first whether built-in TLS, authentication or IPv6 options already cover your need. The guide's examples point the proxy at port 8971. Frigate depends on WebSockets for camera toggles, live playback and other live updates, so the proxy must forward the `Upgrade` and `Connection` headers; Nginx Proxy Manager has a Websockets Support toggle that must be on. Frigate rejects WebSocket connections opened from a page on another site, so the proxy must preserve the original `Host` header or send `X-Forwarded-Host`. The guide has examples for Apache2, Nginx, Caddy, Traefik and others; securing the proxy itself is left to you.

## Checked

Method: docs-checked 2026-11-09 against docs.frigate.video/configuration/tls, docs.frigate.video/guides/reverse_proxy (read as raw markdown from the blakeblackshear/frigate docs folder); documentation only, no commands were run.

Confirmed against those pages: the settings, topics, defaults and procedures described above.

Removed or corrected: Removed the unsupported advice to prefer port 8971 over 5000 and the "(authenticated)" label; the guide only shows its examples proxying to 8971.
