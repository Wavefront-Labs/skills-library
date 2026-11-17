---
id: computing-software.data-engineering.apache-nifi.web-server-limits
name: web-server-limits
category: computing-software
field: data-engineering
product: apache-nifi
tags: [data-engineering, apache-nifi, jetty, web-server, rate-limit, nifi-properties]
level: advanced
status: docs-checked
description: "NiFi web tuning keys and defaults: Jetty threads 200, header size 16 KB, requests per second 30000, access token rate 25, request timeout 60 secs, working directory."
sources:
  - https://nifi.apache.org/docs/nifi-docs/html/administration-guide.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Web server limits

- `nifi.web.jetty.threads`: 200
- `nifi.web.max.header.size`: 16 KB
- `nifi.web.max.content.size`: no default; 20 MB suggested when set
- `nifi.web.max.requests.per.second`: 30000
- `nifi.web.max.access.token.requests.per.second`: 25 (excess login token requests are rejected with HTTP 429)
- `nifi.web.request.timeout`: 60 secs (longer requests are ended with HTTP 503)
- `nifi.web.jetty.working.directory`: `./work/jetty`
- `nifi.web.https.application.protocols`: `http/1.1`
- `nifi.security.user.jws.key.rotation.period`: PT1H (ISO 8601)
- `nifi.ui.autorefresh.interval`: 30 secs

The web request log uses the logger `org.apache.nifi.web.server.RequestLog`.

Verify: a burst test no longer returns throttling errors after you raise the relevant limit.

## Checked

Every key and default above was confirmed in the NiFi Administration Guide: the Web Properties table (Jetty threads 200, max header size 16 KB, max content size with no default and a suggested 20 MB, requests per second 30000, access token requests 25 with HTTP 429, request timeout 60 secs with HTTP 503, working directory, application protocols default http/1.1), the JWS key rotation period of PT1H, and the UI auto refresh interval of 30 secs. Nothing was removed.

Method: docs-only read of cited pages, 2026-11-08
