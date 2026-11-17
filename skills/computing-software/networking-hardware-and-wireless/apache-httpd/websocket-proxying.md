---
id: computing-software.networking-hardware-and-wireless.apache-httpd.websocket-proxying
name: websocket-proxying
category: computing-software
field: networking-hardware-and-wireless
product: apache-httpd
tags: [networking-hardware-and-wireless, apache-httpd, websocket, mod-proxy-wstunnel, ws, wss, upgrade, proxy]
level: practitioner
status: docs-checked
description: "Proxy WebSocket traffic with ws:// and wss:// ProxyPass, mixed HTTP and WebSocket apps, RewriteRule for unknown URLs, and the upgrade parameter."
sources:
  - https://httpd.apache.org/docs/2.4/mod/mod_proxy_wstunnel.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# WebSocket proxying
mod_proxy_wstunnel is deprecated since 2.4.47 because mod_proxy_http handles upgrades; the connection upgrades automatically (response has `Upgrade: WebSocket` and `Connection: Upgrade`).

## Examples
```apache
ProxyPass "/ws2/"  "ws://echo.websocket.org/"
ProxyPass "/wss2/" "wss://echo.websocket.org/"
```
HTTP and WebSocket together, WebSocket rule first:
```apache
ProxyPassMatch ^/(myApp/ws)$  ws://backend.example.com:9080/$1
ProxyPass / http://backend.example.com:9080/
```
URLs not known in advance:
```apache
ProxyPass / http://example.com:9080/
RewriteEngine on
RewriteCond %{HTTP:Upgrade} websocket [NC]
RewriteCond %{HTTP:Connection} upgrade [NC]
RewriteRule ^/?(.*) "ws://example.com:9080/$1" [P,L]
```

## Other
- Balance across backends with mod_proxy_balancer.
- Custom upgrade protocols: `upgrade=` on `ProxyPass`. `upgrade=NONE` and `upgrade=ANY` are for testing only, not production.
- `ProxyWebsocketFallbackToProxyHttp On|Off` (default On) hands requests to mod_proxy_http; Off restores 2.4.46 behaviour.

## Checked

2026-11-08. Deprecation since 2.4.47, ProxyPass ws/wss examples, mixed HTTP and WebSocket rules, RewriteRule form, upgrade parameter including NONE and ANY, and ProxyWebsocketFallbackToProxyHttp (2.4.48 and later, default On) confirmed on the full mod_proxy_wstunnel page. Removed the H2WebSockets claim, which the cited page does not cover.

Method: documentation only; no commands were run.
