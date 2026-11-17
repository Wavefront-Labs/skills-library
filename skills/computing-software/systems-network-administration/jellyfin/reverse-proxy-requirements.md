---
id: computing-software.systems-network-administration.jellyfin.reverse-proxy-requirements
name: reverse-proxy-requirements
category: computing-software
field: systems-network-administration
product: jellyfin
tags: [jellyfin, reverse-proxy, known-proxies, x-forwarded-for, websockets, api-key-logging]
level: practitioner
status: draft
description: "Configure Known Proxies, forwarded headers, WebSockets and log hygiene when running Jellyfin behind a reverse proxy."
sources: ["https://jellyfin.org/docs/general/post-install/networking/8_reverse-proxy/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Reverse proxy requirements

A reverse proxy lets you route by subdomain, geoblock, rate limit and centralise DNS and SSL. Three things must be right for Jellyfin.

**Known proxies.** Behind a proxy Jellyfin sees the proxy's address, not the client's, so it cannot tell local from remote and external-access limits stop working. Put your proxy IP addresses in "Known Proxies" in the Network settings (Dashboard > Advanced > Networking; a restart is requested). Jellyfin then honours `X-Forwarded-For`, `X-Forwarded-Proto` and `X-Forwarded-Host`; by default it discards forwarded-for headers from any other source, so a malicious device cannot hide its address. The proxy must also be configured to send them, which is not always the default. Entries accept subnet masks such as `172.18.0.1/24`, comma separated.

**WebSockets.** Jellyfin uses them; make sure your proxy allows them.

**Logging.** Jellyfin sometimes sends authentication in the URL (the `api_key` parameter). Logging the full request path can write secrets into logs, so protect the logs, do not log full URLs or censor them.

Caddy is the recommended proxy for its ease with HTTPS; guides also exist for Nginx, Traefik, HAProxy and Apache. Replace `DOMAIN_NAME` and `SERVER_IP_ADDRESS` (use 127.0.0.1 on the same host) in examples.

Check: from a remote client, confirm the Dashboard activity shows the real client IP.
