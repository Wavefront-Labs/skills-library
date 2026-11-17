---
id: computing-software.systems-network-administration.coredns.coredns-health-plugin-global
name: coredns-health-plugin-global
category: computing-software
field: systems-network-administration
product: coredns
tags: [coredns, health, healthcheck, lameduck, endpoint]
level: practitioner
status: docs-checked
description: "Enable the process-wide /health endpoint, change its address, and use lameduck to delay shutdown."
sources:
  - https://coredns.io/plugins/health/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: expose a liveness endpoint for CoreDNS.

Syntax:

```
health [ADDRESS] {
    lameduck DURATION
}
```

Facts from the docs:
- The endpoint returns HTTP 200 and the word OK when the server is healthy. Default address is `:8080` and the path is fixed to `/health`.
- health is process wide. If you have several server blocks, enable it in only one of them. To get more endpoints you must put them on different ports, but all of them will export the same health.
- `lameduck DURATION` delays shutdown for the duration. `/health` still answers 200 OK during it, but the ready plugin will not answer OK while CoreDNS is in lame duck mode.
- With the prometheus plugin enabled, health runs a self check once per second, exposing `coredns_health_request_duration_seconds` and `coredns_health_request_failures_total`. A large increase in duration means the process cannot keep up with its query load.

Examples from the docs: `health localhost:8091` in a block runs the endpoint on another address, and `health localhost:8092 { lameduck 1s }` sets a one second lame duck. The health metrics have no `server` label because overload is a symptom of the process, not of one server.

## Checked

2026-11-08. Checked in full against the health plugin README. Removed an unsupported placement gotcha and parser error message; added the documented examples and the metrics label note.

Method: documentation only; no commands were run.
