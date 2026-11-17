---
id: computing-software.systems-network-administration.apache-guacamole.tomcat-remoteipvalve
name: tomcat-remoteipvalve
category: computing-software
field: systems-network-administration
product: apache-guacamole
tags: [systems-network-administration, apache-guacamole, tomcat, remoteipvalve, internalproxies, x-forwarded-for, client-ip, server-xml, urlencoding, reverse-proxy]
level: practitioner
status: docs-checked
description: "Configure Tomcat's RemoteIpValve and HTTP connector so Guacamole sees real client IPs behind a reverse proxy and handles UTF-8 names."
sources:
  - https://guacamole.apache.org/doc/gug/reverse-proxy.html
  - https://guacamole.apache.org/doc/gug/troubleshooting.html
  - https://guacamole.apache.org/doc/gug/guacamole-docker.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tomcat RemoteIpValve

Without it every user appears to come from the proxy IP, which undermines auditing of logins and connections and anything keyed on client address. In `conf/server.xml`, inside `<Host>`:

```xml
<Valve className="org.apache.catalina.valves.RemoteIpValve"
       internalProxies="127\.0\.0\.1|0:0:0:0:0:0:0:1"
       remoteIpHeader="x-forwarded-for"
       remoteIpProxiesHeader="x-forwarded-by"
       protocolHeader="x-forwarded-proto" />
```
- `internalProxies`: regex of proxy IPs trusted to set the headers. Include both IPv4 and IPv6 loopback even for a same-host proxy. If the proxy is on another host or Docker network, use its real address.
- Trust only proxies you control; `X-Forwarded-For` is spoofable.
- Guacamole reads the result via `request.getRemoteAddr()`.

Connector: keep plain HTTP (AJP is unsupported: no WebSocket, and Apache 2.4.3 and older lacks PATCH over AJP) and set UTF-8:
```xml
<Connector port="8080" protocol="HTTP/1.1" connectionTimeout="20000"
           URIEncoding="UTF-8" redirectPort="8443" />
```
Missing `URIEncoding` makes Unicode-named connections report as nonexistent.

Docker equivalent: `REMOTE_IP_VALVE_ENABLED=true` (required; other valve variables are ignored without it) and optional `PROXY_ALLOWED_IPS_REGEX` (default: Tomcat's, which matches private IPv4 and IPv6 addresses); see apache-guacamole.docker-guacamole-webapp.

Verify: the Active Sessions or History view shows real client addresses.

## Checked

2026-11-08. Read the whole of reverse-proxy.html and the UTF-8 passage of troubleshooting.html (partial read, that section only), plus the proxy section of guacamole-docker.html (partial read). Confirmed the valve attributes and both example regexes, the trust and spoofing warning, getRemoteAddr(), the connector entry, URIEncoding symptom and the Docker variables. Removed the claim that missing client IPs break brute-force banning and host restrictions by name (the page says the IP is used for auditing and possibly authentication).
Method: documentation only; no commands were run.
