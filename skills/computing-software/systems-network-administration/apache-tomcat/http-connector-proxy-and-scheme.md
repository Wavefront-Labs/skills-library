---
id: computing-software.systems-network-administration.apache-tomcat.http-connector-proxy-and-scheme
name: http-connector-proxy-and-scheme
category: computing-software
field: systems-network-administration
product: apache-tomcat
tags: [computing-software, systems-network-administration, apache-tomcat, tomcat, http-connector, proxyname, proxyport, scheme, secure, redirectport, useipvhosts, server-header, allowtrace]
level: practitioner
status: docs-checked
description: "Connector attributes that shape what apps see behind a proxy or on SSL: proxyName, proxyPort, scheme, secure, redirectPort, useIPVHosts, server header, allowTrace, enableLookups."
sources:
  - https://tomcat.apache.org/tomcat-10.1-doc/config/http.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Proxy, scheme and header attributes on the HTTP Connector

| Attribute | Default | Effect |
|---|---|---|
| `proxyName` | none | Returned by `request.getServerName()` |
| `proxyPort` | none | Returned by `request.getServerPort()` |
| `scheme` | http | Forced to https when `SSLEnabled="true"` |
| `secure` | false | Forced to true when `SSLEnabled="true"` |
| `redirectPort` | none | Target when a non-SSL request hits a `<security-constraint>` needing SSL |
| `useIPVHosts` | false | true selects the virtual host by the IP the request arrived on |
| `strictSni` | true | Rejects requests whose SNI and Host header map to different `SSLHostConfig`s |
| `server` | unset | Overrides the `Server` response header (also overrides app-set values) |
| `serverRemoveAppProvidedValues` | false | Strip app-set `Server` headers; ignored if `server` is set |
| `xpoweredBy` | false | Advertises Servlet specification support using the header the specification recommends |
| `allowTrace` | false | Enables TRACE (cookie and authorization headers are excluded from the response) |
| `enableLookups` | false | true makes `getRemoteHost()` do DNS lookups |

Example: Tomcat behind a TLS-terminating proxy that talks plain HTTP on 8080 (fixed values; for per-request forwarded headers use `computing-software.systems-network-administration.apache-tomcat.remote-ip-valve`):
```xml
<Connector port="8080" protocol="HTTP/1.1" proxyName="www.example.com"
           proxyPort="443" scheme="https" secure="true" server="web"/>
```

## Checked

2026-11-04. Confirmed against the Tomcat 10.1 HTTP Connector reference: attribute names and defaults. Reworded allowTrace and xpoweredBy; removed the generic verify line.

Method: documentation only; no commands were run.
