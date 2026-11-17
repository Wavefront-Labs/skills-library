---
id: computing-software.messaging-and-integration.nats.monitoring-endpoint
name: monitoring-endpoint
category: computing-software
field: messaging-and-integration
product: nats
tags: [monitoring, http-port, varz, prometheus-exporter, monitor-port, https-port]
level: practitioner
status: docs-checked
description: "Turn on the nats-server HTTP monitoring port with -m or http_port, and avoid exposing it, since it has no authentication."
sources:
  - https://github.com/nats-io/nats.docs/blob/master/running-a-nats-service/configuration/monitoring.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: expose server statistics over HTTP and scrape them safely.

Enable from the command line with `-m/--http_port PORT` (HTTP) or `-ms/--https_port PORT` (HTTPS), for example `nats-server -m 8222`; startup logs "Starting http monitor on port 8222". In the config file: `http_port: 8222`, or bind locally with `http: localhost:8222`. Then browse `http://localhost:8222/` or `http://localhost:8222/varz` for general statistics. Other endpoints are described in the monitoring reference.

Endpoints support JSONP and CORS, making single-page dashboards easy. For metrics collection the docs point to the Prometheus NATS Exporter (github.com/nats-io/prometheus-nats-exporter), which lets you pick what to export.

Security warning from the page: the monitoring endpoint has no authentication or authorization. When a server is open to the internet, do not expose the monitoring port; by default it binds to every interface, so bind to localhost or firewall it.

Notes: a root-level `tls` block also secures the monitoring port when `https_port` is used. With `verify` client certificates, monitoring is excluded so browsers can use it.

## Checked

2026-11-03. Read against the nats.docs repository (the pages listed in `sources`, plus the neighbouring concept, release-note and nsc/nk tool pages): configuration keys, flags, CLI commands, defaults, limits, subjects, header names and version gates were confirmed there.
Removed: the unsourced Verify step, plus statements that no page supports (see the PR notes for the per-skill list).
Method: documentation only; no commands were run.
