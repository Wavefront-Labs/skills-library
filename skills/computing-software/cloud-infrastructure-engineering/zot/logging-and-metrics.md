---
id: computing-software.cloud-infrastructure-engineering.zot.logging-and-metrics
name: logging-and-metrics
category: computing-software
field: cloud-infrastructure-engineering
product: zot
tags: [zot, prometheus-metrics, log-level, audit-log, zxp, metrics-access]
level: practitioner
status: docs-checked
description: "Configure Zot logging (level, output, audit) and Prometheus metrics for full images or minimal images with zxp, including anonymous scrape access."
sources:
  - https://raw.githubusercontent.com/project-zot/project-zot.github.io/main/docs/articles/monitoring.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Logging, the `log` block:
- `level`: `panic`, `fatal`, `error`, `warn`, `info`, `debug` or `trace`.
- `output`: file path; defaults to `stdout`.
- `audit`: optional path that enables audit logging.

Metrics, full image: `extensions.metrics`:

```json
"metrics": { "enable": true, "prometheus": { "path": "/metrics" } }
```

- On if the key is absent; `enable: false` turns it off.
- `path` must be a clean absolute path starting with `/`; reserved or broad paths such as `/` and `/v2` are rejected by validation.

Minimal image: exposes Prometheus-format internal metrics, scraped by the separate `zxp` exporter. Metrics turn on at the first scrape and off after a period without scraping. Configure with `zxp-<platform> config zxp-config-file` (keys `Server.protocol`, `Server.host`, `Server.port`, `Exporter.port`, `Exporter.log.level`); a sample Dockerfile is `build/Dockerfile-zxp`. `zxp` is not needed with a full image.

Access control: `accessControl.metrics.users` lists users who may read metrics; `metrics.anonymousPolicy: ["read"]` lets unauthenticated scrapers in. Authenticated users not listed are denied even if anonymous read is enabled.

## Checked

2026-11-04. Read against the zot monitoring article. Removed: the prometheus readTimeout and writeTimeout 60s defaults, not stated on the page.

Method: documentation only; no commands were run.
