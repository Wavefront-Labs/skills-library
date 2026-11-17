---
id: computing-software.systems-network-administration.apache-tomcat.crawler-session-manager-valve
name: crawler-session-manager-valve
category: computing-software
field: systems-network-administration
product: apache-tomcat
tags: [computing-software, systems-network-administration, apache-tomcat, tomcat, valve, crawlersessionmanagervalve, crawler, bot-sessions, session-memory, crawleruseragents]
level: practitioner
status: docs-checked
description: "Stop web crawlers from creating thousands of Tomcat 10.1 sessions with CrawlerSessionManagerValve: user-agent regex, crawlerIps, sessionInactiveInterval, contextAware, hostAware."
sources:
  - https://tomcat.apache.org/tomcat-10.1-doc/config/valve.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# CrawlerSessionManagerValve

Class `org.apache.catalina.valves.CrawlerSessionManagerValve`. Makes each crawler (by client IP plus matching user agent) share one session instead of creating a session per request.

| Attribute | Default |
|---|---|
| `crawlerUserAgents` | `.*[bB]ot.*|.*Yahoo! Slurp.*|.*Feedfetcher-Google.*` |
| `crawlerIps` | none (no IP check) |
| `sessionInactiveInterval` | 60 seconds |
| `contextAware` | true |
| `hostAware` | true |

```xml
<Valve className="org.apache.catalina.valves.CrawlerSessionManagerValve"
       sessionInactiveInterval="600"/>
```

Rules:
- Place it after RemoteIpValve so the real client IP is used (`computing-software.systems-network-administration.apache-tomcat.remote-ip-valve`).
- Choose `crawlerUserAgents` with care: the page warns crawlers must not be associated with the authenticated session of a genuine user. The valve tries, but does not guarantee, to detect this and expire the authenticated session.
- `crawlerIps` is a regular expression matched against the client IP; an IP match alone is enough to treat the request as a crawler, and by default no IP check is made.
- May be used at Engine, Host or Context level; normally Engine.

## Checked

2026-11-04. Confirmed against the Tomcat 10.1 Valve reference (Crawler Session Manager Valve): attributes, defaults, ordering after RemoteIpValve. Corrected crawlerIps (it adds a match, it does not restrict one). Removed the spoofing claim and the generic verify line.

Method: documentation only; no commands were run.
