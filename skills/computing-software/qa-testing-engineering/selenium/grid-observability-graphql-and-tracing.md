---
id: computing-software.qa-testing-engineering.selenium.grid-observability-graphql-and-tracing
name: grid-observability-graphql-and-tracing
category: computing-software
field: qa-testing-engineering
product: selenium
tags: [grid-graphql, selenium-grid, opentelemetry, grid-observability, jaeger]
level: practitioner
status: docs-checked
description: "Observe Selenium Grid: query sessions, slots and queue via the GraphQL endpoint, enable OpenTelemetry tracing to Jaeger, and read event logs to debug stuck sessions."
sources:
  - https://www.selenium.dev/documentation/grid/advanced_features/graphql_support/
  - https://www.selenium.dev/documentation/grid/advanced_features/observability/
  - https://www.selenium.dev/documentation/grid/advanced_features/endpoints/
  - https://www.selenium.dev/documentation/grid/configuration/cli_options/
  - https://github.com/SeleniumHQ/docker-selenium/blob/trunk/ENV_VARIABLES.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Grid observability (tracing, GraphQL status)

## GraphQL endpoint (`/graphql`)
```bash
curl -s -X POST -H "Content-Type: application/json" http://grid.example.test:4444/graphql \
  --data '{"query":"{ grid { totalSlots, sessionCount, maxSession, sessionQueueSize, nodeCount } }"}'

curl -s -X POST -H "Content-Type: application/json" http://grid.example.test:4444/graphql \
  --data '{"query":"{ nodesInfo { nodes { id, uri, status, maxSession, sessionCount, slotCount, stereotypes } } }"}'

curl -s -X POST -H "Content-Type: application/json" http://grid.example.test:4444/graphql \
  --data '{"query":"{ sessionsInfo { sessionQueueRequests, sessions { id, capabilities, startTime, nodeUri, sessionDurationMillis } } }"}'
```
Use cases: CI pre-check that slots exist, dashboards, and finding long-running sessions (`sessionDurationMillis`).

## Delete a stuck session
Through the Grid URL: `curl -X DELETE http://grid:4444/session/<sessionId>`. Directly on the node: `curl -X DELETE http://node:5555/se/grid/node/session/<sessionId> -H 'X-REGISTRATION-SECRET: <secret>'`; drain a node: `curl -X POST http://node:5555/se/grid/node/drain -H 'X-REGISTRATION-SECRET: <secret>'`.

## Tracing (OpenTelemetry)
Tracing uses OpenTelemetry and is enabled by default (`--tracing`, default `true`). Spans are logged at FINE level by the console exporter, so run with `--log-level FINE` to see them; for the Jaeger setup steps run `java -jar selenium-server-<version>.jar info tracing`. In docker-selenium, `SE_ENABLE_TRACING` maps to `--tracing` and `SE_OTEL_EXPORTER_ENDPOINT` to `-Dotel.exporter.otlp.endpoint=`.
Each request is traced across the Grid components, so you can see where time goes (queueing vs browser).

## Logs
- `--log-level FINE` and `--structured-logs` (default `false`) for structured logs.
- Correlate test failures with session id (print `driver.getSessionId()` in test logs).

## Metrics worth alerting on
Queue size (`sessionQueueSize`) above zero for a sustained period, slot utilisation near 100% (`sessionCount` against `totalSlots`), and `nodeCount` dropping.

## Gotchas
- GraphQL and the UI expose capabilities that may include credentials passed as capabilities; avoid secrets in capabilities.

## Verify
A dashboard shows queue, slots and sessions, and a trace for a slow test reveals whether time was spent queuing or in the browser.

## Checked

Checked 2026-10-25 against the Selenium documentation source (seleniumhq.github.io, pushed 2026-10-23, examples tracking Selenium 4.51) and the docker-selenium repository (pushed 2026-10-20, README, ENV_VARIABLES.md and the selenium-grid chart README and values.yaml, images tagged 4.51.0-20261010). Confirmed: the GraphQL schema fields used in all three queries; the node session delete and drain endpoints and the `X-REGISTRATION-SECRET` header; `--tracing` default true, `--log-level`, `--structured-logs`; docker-selenium `SE_ENABLE_TRACING` and `SE_OTEL_EXPORTER_ENDPOINT` mappings. Corrected: the header was written `'X-REGISTRATION-SECRET;'` (sends an empty value); the Jaeger java -D and coursier command line replaced with the documented `info tracing` route. Removed: event bus log claims, overhead and sampling advice.

Method: documentation only; no commands were run.
