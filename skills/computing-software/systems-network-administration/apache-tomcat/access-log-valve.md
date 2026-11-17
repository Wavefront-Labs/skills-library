---
id: computing-software.systems-network-administration.apache-tomcat.access-log-valve
name: access-log-valve
category: computing-software
field: systems-network-administration
product: apache-tomcat
tags: [computing-software, systems-network-administration, apache-tomcat, tomcat, valve, accesslogvalve, access-log, log-pattern, combined, rotation, maxdays, request-time]
level: practitioner
status: docs-checked
description: "Configure AccessLogValve in Tomcat 10.1: directory, prefix/suffix, pattern codes (%h %t %r %s %b %D %I), common/combined, daily rotation, maxDays, conditional logging."
sources:
  - https://tomcat.apache.org/tomcat-10.1-doc/config/valve.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# AccessLogValve

Class `org.apache.catalina.valves.AccessLogValve`; nest in Engine, Host or Context.

| Attribute | Default |
|---|---|
| `directory` | logs (relative to `$CATALINA_BASE`) |
| `prefix` / `suffix` | access_log / empty |
| `pattern` | `common`, `combined` or custom |
| `fileDateFormat` | .yyyy-MM-dd (rotation happens when the formatted time changes) |
| `rotatable` | true (false: no timestamp, no rotation) |
| `renameOnRotate` | false |
| `maxDays` | -1 (never delete) |
| `buffered` | true |
| `encoding` | UTF-8 |
| `ipv6Canonical` | false |
| `requestAttributesEnabled` | false (true uses RemoteIpValve attributes) |
| `condition` / `conditionIf` / `conditionUnless` | none |

Codes: `%h` remote host, `%l` identd (always -), `%u` user, `%t` time, `%r` request line, `%s` status, `%b` bytes or -, `%B` bytes or 0, `%D` time in microseconds, `%T` time in seconds, `%I` thread name. Unknown codes print `???X???`.
`common` = `%h %l %u %t "%r" %s %b`; `combined` adds Referer and User-Agent.

```xml
<Valve className="org.apache.catalina.valves.AccessLogValve"
       directory="logs" prefix="localhost_access_log" suffix=".txt"
       pattern='%h %l %u %t "%r" %s %b %D' maxDays="14"
       requestAttributesEnabled="true"/>
```

Behind a proxy add the RemoteIpValve and set `requestAttributesEnabled="true"` so the real client IP is logged. Hostname lookups: use the Connector `enableLookups`, or `%a` rather than `%h`.

## Checked

2026-11-04. Confirmed against the Tomcat 10.1 Valve reference (Access Log Valve): attribute names and defaults, pattern codes, common/combined shorthands, unknown-code output, resolveHosts note. Removed the generic verify line.

Method: documentation only; no commands were run.
