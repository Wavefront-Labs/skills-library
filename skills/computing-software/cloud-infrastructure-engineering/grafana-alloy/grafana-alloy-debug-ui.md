---
id: computing-software.cloud-infrastructure-engineering.grafana-alloy.grafana-alloy-debug-ui
name: grafana-alloy-debug-ui
category: computing-software
field: cloud-infrastructure-engineering
product: grafana-alloy
tags: [alloy-ui, debug-ui, graph-page, clustering-page, component-detail, live-debugging, localhost-12345]
level: intro
status: docs-checked
description: "Use the Alloy debug UI pages, know which components support live debugging, and expose the UI."
sources: ["https://github.com/grafana/alloy/blob/main/docs/sources/troubleshoot/debug.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# The Alloy debug UI

The embedded UI is served by the HTTP server at `http://localhost:12345`. Non-containerized installs listen on localhost only, so other machines cannot see it; to expose it, follow the install docs for your platform or the `run` command reference for the HTTP listen address.

## Pages
- **Home**: table of components and their health; **View** opens the detail page.
- **Graph**: draggable component graph; modules have their own graph button. Edges show data volume leaving components that support live debugging, refreshed by the `window` parameter.
- **Component detail**: health with message, evaluated arguments, exports and debug info. Secrets display as `(secret)`. Links to the docs and live debugging.
- **Clustering**: each node's name, advertised address, state (Viewer, Participant, Terminating) and which node serves the UI.
- **Live debugging**: real-time data stream from a component. Pause, clear, sample, stop auto-scroll, search and copy. Disabled by default to avoid displaying sensitive telemetry; enable it by configuring the `livedebugging` block.

Components supporting live debugging: `loki.process`, `loki.relabel`, `loki.secretfilter`, `otelcol.connector.*`, `otelcol.processor.*`, `otelcol.receiver.*`, `prometheus.remote_write`, `prometheus.relabel`, `discovery.*`, `prometheus.scrape`.

## Workflow
1. Check no component is unhealthy.
2. Check arguments and exports of the misbehaving component.
3. Check the live debugging data.
4. Only then read logs.

## Checked

2026-11-08. Read in full the raw Alloy docs page behind the cited URL (docs/sources/troubleshoot/debug.md): UI pages, localhost default, live debugging caution and supported components list, and the debug-using-the-UI steps. Removed the `--server.http.listen-addr` flag name, `enabled = true` and the TLS remark, which that page does not state.

Method: documentation only; no commands were run.
