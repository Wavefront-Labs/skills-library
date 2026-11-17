---
id: computing-software.systems-network-administration.apache-guacamole.apache-httpd-reverse-proxy
name: apache-httpd-reverse-proxy
category: computing-software
field: systems-network-administration
product: apache-guacamole
tags: [systems-network-administration, apache-guacamole, apache-httpd, reverse-proxy, mod-proxy, mod-proxy-wstunnel, flushpackets, websocket-tunnel, ssl-termination]
level: practitioner
status: docs-checked
description: "Proxy Guacamole behind Apache httpd with mod_proxy and mod_proxy_wstunnel: Location blocks, flushpackets=on, block order, quieter logs."
sources:
  - https://guacamole.apache.org/doc/gug/reverse-proxy.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Apache httpd reverse proxy

Enable `mod_proxy` and `mod_proxy_wstunnel` (needs Apache 2.4.5+). Without wstunnel Guacamole falls back to the HTTP tunnel.

```apache
<Location /guacamole/>
    Order allow,deny
    Allow from all
    ProxyPass http://HOSTNAME:8080/guacamole/ flushpackets=on
    ProxyPassReverse http://HOSTNAME:8080/guacamole/
</Location>

<Location /guacamole/websocket-tunnel>
    Order allow,deny
    Allow from all
    ProxyPass ws://HOSTNAME:8080/guacamole/websocket-tunnel
    ProxyPassReverse ws://HOSTNAME:8080/guacamole/websocket-tunnel
</Location>
```
Rules:
- `flushpackets=on` is required for the HTTP tunnel.
- The `websocket-tunnel` block must come after `/guacamole/`: Apache honours the last matching section.
- Apache forwards `X-Forwarded-For` by default; Tomcat needs the RemoteIpValve to use it (see apache-guacamole.tomcat-remoteipvalve).

Reduce log noise from tunnel polling:
```apache
SetEnvIf Request_URI "^/guacamole/tunnel" dontlog
CustomLog /var/log/apache2/guac.log common env=!dontlog
```
Adjust the URI if Guacamole is served at another path.

Verify: browser developer tools show a WebSocket upgrade to `websocket-tunnel`.

## Checked

2026-11-08. Read the whole of the reverse proxy page (reverse-proxy.html) and confirmed the mod_proxy and mod_proxy_wstunnel requirement (Apache 2.4.5 and later), the Location blocks, flushpackets=on, last-match ordering for the websocket-tunnel block, Apache passing X-Forwarded-For by default, and the SetEnvIf logging example. Nothing removed.
Method: documentation only; no commands were run.
