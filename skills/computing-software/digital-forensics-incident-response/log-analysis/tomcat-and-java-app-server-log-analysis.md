---
id: computing-software.digital-forensics-incident-response.log-analysis.tomcat-and-java-app-server-log-analysis
name: tomcat-and-java-app-server-log-analysis
category: computing-software
field: digital-forensics-incident-response
product: log-analysis
tags: [tomcat-logs, log4shell, java-app-server, web-logs, dfir]
level: practitioner
status: draft
description: "Investigate Tomcat and Java application server logs: access log valves, catalina and manager logs, WAR deployment webshells, and Log4Shell JNDI exploitation traces."
sources: ["https://tomcat.apache.org/tomcat-10.1-doc/config/valve.html#Access_Log_Valve", "https://tomcat.apache.org/tomcat-10.1-doc/logging.html", "https://www.cisa.gov/news-events/news/apache-log4j-vulnerability-guidance"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Tomcat and Java application server logs

## Locations (default `$CATALINA_BASE/logs/`)
| File | Content |
|---|---|
| `localhost_access_log.<date>.txt` | AccessLogValve (common format by default; often no User-Agent) |
| `catalina.<date>.log` / `catalina.out` | Server lifecycle, deployment, stack traces (stdout of webapps on many installs) |
| `localhost.<date>.log` | Webapp context errors |
| `manager.<date>.log` / `host-manager.*` | Manager app actions |

## Attack patterns
- **Manager WAR upload**: `POST /manager/text/deploy?path=/x` or `/manager/html/upload` with 200, followed by catalina log `Deploying web application archive [.../webapps/x.war]`, then GETs to `/x/<name>.jsp?cmd=`. Check `tomcat-users.xml` for added users and the 401 brute force before success.
- **JSP webshells**: new `.jsp` under `webapps/*/`; access log requests with `cmd=`, `pwd=`, POST-heavy small URIs. Compare webapp file mtimes.
- **Log4Shell (CVE-2021-44228)**: strings like `${jndi:ldap://`, obfuscated `${${lower:j}ndi:` / `${${::-j}${::-n}di:` in any logged field (URI, User-Agent, headers in app logs). Confirm exploitation via outbound LDAP/RMI/DNS from the JVM host, not by the string alone.
- **Ghostcat (CVE-2020-1938)**: AJP port 8009 exposed; reads of `WEB-INF/web.xml`.
- **Deserialisation / Struts / Spring4Shell**: stack traces in catalina logs (`ClassCastException`, `ognl`) around the request time.

```bash
grep -RhoE '\$\{[^}]*(jndi|lower|upper|::-)[^ ]*' logs/ app-logs/ | sort | uniq -c | sort -rn | head
grep -h 'manager/' logs/localhost_access_log* | awk '{print $1,$4,$6,$7,$9}'
```

## Gotchas
- Default access log omits User-Agent and processing time: set `pattern="combined"` (or `%{User-Agent}i %D`) for readiness.
- Behind a proxy, the client IP is in X-Forwarded-For; configure `RemoteIpValve`.

## Verify
Each exploitation hypothesis is backed by both an inbound request and a host-side effect (deployed file, process, outbound connection).
