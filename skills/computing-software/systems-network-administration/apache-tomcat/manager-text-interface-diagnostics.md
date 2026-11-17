---
id: computing-software.systems-network-administration.apache-tomcat.manager-text-interface-diagnostics
name: manager-text-interface-diagnostics
category: computing-software
field: systems-network-administration
product: apache-tomcat
tags: [computing-software, systems-network-administration, apache-tomcat, tomcat, manager, text-interface, sessions, expire, serverinfo, threaddump, vminfo, findleaks, sslreload, resources]
level: practitioner
status: docs-checked
description: "Diagnostic commands of the Tomcat 10.1 Manager text interface: sessions, expire, serverinfo, resources, threaddump, vminfo, findleaks, TLS listing, sslReload, save."
sources:
  - https://tomcat.apache.org/tomcat-10.1-doc/manager-howto.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Manager text interface: diagnostics

Commands are usually executed by HTTP GET under `/manager/text/`; the text interface needs the `manager-script` role.

| Command | URL | Notes |
|---|---|---|
| sessions | `/sessions?path=/app` | Default session timeout and active sessions in one-minute ranges of their timeout |
| expire | `/expire?path=/app&idle=30` | Expire sessions idle over N minutes; `idle=0` expires all (same command as sessions) |
| serverinfo | `/serverinfo` | Tomcat, OS and JVM properties |
| resources | `/resources?type=javax.sql.DataSource` | Global JNDI resources; type optional |
| threaddump | `/threaddump` | JVM thread dump |
| vminfo | `/vminfo` | JVM and OS diagnostics |
| findleaks | `/findleaks?statusLine=true` | Lists apps that leaked when stopped, reloaded or undeployed; triggers a full GC, use with extreme caution in production; confirm with a profiler |
| sslConnectorCiphers | `/sslConnectorCiphers` | Ciphers per connector |
| sslConnectorCerts | `/sslConnectorCerts` | Certificate chain per connector |
| sslConnectorTrustedCerts | `/sslConnectorTrustedCerts` | Trusted certs per connector |
| sslReload | `/sslReload?tlsHostName=name` | Reloads the certificate and key files (no re-parse of server.xml); omit the name for all hosts |
| save | `/save` | Save server.xml; with `path`, that app's context.xml; needs the StoreConfig MBean |

```bash
curl -u ops:<pw> "http://localhost:8080/manager/text/threaddump"
curl -u ops:<pw> "http://localhost:8080/manager/text/sslReload?tlsHostName=www.example.com"
```

Responses are text/plain and start with `OK` or `FAIL`.

## Checked

2026-11-04. Confirmed against the Tomcat 10.1 Manager how-to (sessions, expire, resources, findleaks, SSL connector diagnostics, sslReload, threaddump, vminfo, save). Reworded sessions, findleaks and sslReload; removed the certificate-rotation claim and the generic verify line.

Method: documentation only; no commands were run.
