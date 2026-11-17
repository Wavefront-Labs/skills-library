---
id: computing-software.cloud-infrastructure-engineering.grafana-loki-tempo.alloy-ui-fmt-and-debugging
name: alloy-ui-fmt-and-debugging
category: computing-software
field: cloud-infrastructure-engineering
product: grafana-loki-tempo
tags: [alloy-debugging, alloy, alloy-ui, live-debugging, component-health, clustering]
level: practitioner
status: docs-checked
description: "Debug Alloy with its UI, live debugging, component health and logs; find why data is not flowing."
sources: ["https://grafana.com/docs/alloy/latest/troubleshoot/debug/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: a systematic path from "no data" to the failing component.

1. Open the embedded UI served by the Alloy HTTP server, by default at `http://localhost:12345`. On non-containerized installs it listens on localhost only, for security, so other machines cannot view it; change the listen address through the `alloy run` flags or your install method's docs.
2. The home page lists components and their health. The component detail page shows the health with an explanatory message, current evaluated arguments, current exports and, if the component has it, debug info. Secret values display only as `(secret)`.
3. The Graph page (experimental) shows components and their connections; edges show the amount of data leaving components that support live debugging.
4. Live debugging gives a real-time stream of data from a component. It is disabled by default to avoid exposing sensitive telemetry; enable it with the `livedebugging` block:
```
livedebugging {
  enabled = true
}
```
Then open the Live Debugging page from the component detail page. You can pause and clear the stream, sample data, search by keyword and copy the stream. Supported components include `loki.process`, `loki.relabel`, `loki.secretfilter`, `otelcol.receiver.*`, `otelcol.processor.*`, `otelcol.connector.*`, `prometheus.remote_write`, `prometheus.relabel`, `prometheus.scrape` and `discovery.*`.
5. If the UI does not explain the problem, read the logs. Set the level with the `logging` block; the default format is `logfmt` and `json` is also available.

Debug using the UI: make sure no component is unhealthy, that arguments and exports of the misbehaving component look right, and that the live debugging data matches expectations.

Clustering symptoms to check on each peer's UI clustering page: cluster not converging (usually network connectivity), split brain (peers unaware of each other; check join addresses are formatted correctly and reachable), configuration drift (nodes must run the same configuration), node name conflicts (the cluster rejects duplicates) and a node stuck in the Terminating state. Missing metrics can also come from scraping or discovery problems rather than clustering.

## Verify
After the fix, the failing component reports healthy in the UI and live debugging shows data passing through.

## Checked
Method: docs-checked 2026-11-09 against the Alloy docs debug page (raw markdown, read in full). Unconfirmed pprof, metrics-grep, reload and fmt steps were dropped.
