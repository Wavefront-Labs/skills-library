---
id: computing-software.systems-network-administration.immich.structured-logging
name: structured-logging
category: computing-software
field: systems-network-administration
product: immich
tags: [immich-log-format, json-logs, loki, log-level, no-color]
level: practitioner
status: docs-checked
description: "Switch Immich logs to structured JSON with IMMICH_LOG_FORMAT for Loki, ELK, Datadog or Splunk, and tune level and colour."
sources:
  - https://docs.immich.app/features/monitoring
  - https://docs.immich.app/install/environment-variables
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: emit machine-parseable logs for aggregation systems.

By default Immich writes human-readable console logs. Set this in `.env` for JSON:

```
IMMICH_LOG_FORMAT=json
```

The default is `console`. The docs recommend `json` for production deployments that use log aggregation such as Grafana Loki, ELK Stack, Datadog or Splunk.

Each line is a JSON object:

```json
{"level":"warn","pid":48,"timestamp":1766533331629,"message":"Unable to open /build/www/index.html, skipping SSR.","context":"ApiService"}
```

Fields:

- `level`: log, warn, error and so on.
- `pid`: process ID.
- `timestamp`: Unix timestamp in milliseconds.
- `message`: the log text.
- `context`: the service or component that logged it.

Related variables from the environment variable reference:

- `IMMICH_LOG_LEVEL`: one of verbose, debug, log, warn, error.
- `NO_COLOR`: set to `true` to disable colour-coded output.

`IMMICH_LOG_LEVEL` defaults to `log`. `IMMICH_LOG_FORMAT` applies to the server; `NO_COLOR` applies to the server and machine learning.

## Checked

2026-11-09. Read the Monitoring page (Structured Logging section) and the environment variables page in full and checked the variables, defaults, JSON example and field list against them. Removed the admin-settings and config-file logging claim and the docker logs commands, which neither page states.

Method: documentation only; no commands were run.
