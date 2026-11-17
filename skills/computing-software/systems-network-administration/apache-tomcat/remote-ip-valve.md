---
id: computing-software.systems-network-administration.apache-tomcat.remote-ip-valve
name: remote-ip-valve
category: computing-software
field: systems-network-administration
product: apache-tomcat
tags: [computing-software, systems-network-administration, apache-tomcat, tomcat, valve, remoteipvalve, x-forwarded-for, internalproxies, trustedproxies, reverse-proxy, client-ip, x-forwarded-proto]
level: advanced
status: docs-checked
description: "Use RemoteIpValve in Tomcat 10.1 behind a reverse proxy: remoteIpHeader, internalProxies, trustedProxies, protocolHeader, port/host headers and request attributes."
sources:
  - https://tomcat.apache.org/tomcat-10.1-doc/config/valve.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# RemoteIpValve

Class `org.apache.catalina.valves.RemoteIpValve`. Replaces the apparent client IP and scheme using proxy headers.

| Attribute | Default |
|---|---|
| `remoteIpHeader` | x-forwarded-for |
| `proxiesHeader` | x-forwarded-by |
| `internalProxies` | regex of private/loopback/link-local/CGNAT ranges (10/8, 192.168/16, 169.254/16, 127/8, 100.64/10, 172.16/12, ::1, fe80::, fc/fd) |
| `trustedProxies` | none (none trusted) |
| `protocolHeader` | X-Forwarded-Proto (empty string disables) |
| `protocolHeaderHttpsValue` | https |
| `hostHeader`, `portHeader` | null |
| `httpServerPort` / `httpsServerPort` | 80 / 443 |
| `changeLocalName`, `changeLocalPort` | false |
| `requestAttributesEnabled` | true (sets `org.apache.catalina.AccessLog.*`) |

Example for a single proxy at 10.0.0.5:
```xml
<Valve className="org.apache.catalina.valves.RemoteIpValve"
       internalProxies="10\.0\.0\.5"
       remoteIpHeader="X-Forwarded-For"
       protocolHeader="X-Forwarded-Proto"/>
```

Security: the first (outermost) proxy must strip incoming `x-forwarded-for`, `x-forwarded-by`, `x-forwarded-proto`, `x-forwarded-host` and `x-forwarded-port` from untrusted requests, or clients can spoof their address. The default `internalProxies` assumes all local networks are trusted; adjust it if that is not the case. Copy the default regex from the official page rather than retyping it.

May be used at Engine, Host or Context level (normally Engine); define it before Remote Address/Host valves.

Pair with `computing-software.systems-network-administration.apache-tomcat.access-log-valve` (`requestAttributesEnabled="true"`).

## Checked

2026-11-04. Confirmed against the Tomcat 10.1 Valve reference (Remote IP Valve): attribute names, defaults, header list, request attributes, security section. Removed the generic verify line.

Method: documentation only; no commands were run.
