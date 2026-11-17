---
id: computing-software.systems-network-administration.healthchecks.ping-url-overview
name: ping-url-overview
category: computing-software
field: systems-network-administration
product: healthchecks
tags: [healthchecks, ping-url, pinging-api, ping-body-limit, heartbeat-monitoring]
level: intro
status: docs-checked
description: "How the Healthchecks Pinging API works: supported protocols and methods, the 200 OK response, the Ping-Body-Limit header and the five signal types."
sources:
  - https://raw.githubusercontent.com/healthchecks/healthchecks/master/templates/docs/http_api.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The Pinging API receives signals from your jobs: success, start, failure, log and exit status.

Transport:
- HTTP and HTTPS, HTTP 1.0, 1.1 and 2, IPv4 and IPv6.
- Methods HEAD, GET and POST. Only POST should carry a body (diagnostic text). If the body looks like UTF-8, the server stores up to its body limit per ping.
- Success is HTTP 200 with the body `OK`.
- Responses can include a `Ping-Body-Limit: <n>` header: how many body bytes are stored per request. Extra bytes are ignored.

Signals, appended to a check's ping URL:
- success: the bare URL (job finished, or a long-running process is healthy)
- start: `/start`
- failure: `/fail`
- log: `/log`
- exit status: `/<exit-status>`

A check is addressed either by its UUID or by project ping key plus slug (`<ping-key>/<slug>`). Treat UUIDs and ping keys as secrets, since anyone holding them can send signals to your checks.

## Checked

2026-11-04: confirmed against the Pinging API page (protocols, methods, 200 OK, Ping-Body-Limit header, endpoint list) and the Slug URLs page (UUIDs and ping keys are secrets).
Method: documentation only; no commands were run.
