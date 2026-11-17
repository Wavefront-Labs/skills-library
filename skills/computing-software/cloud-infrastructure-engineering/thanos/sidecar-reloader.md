---
id: computing-software.cloud-infrastructure-engineering.thanos.sidecar-reloader
name: sidecar-reloader
category: computing-software
field: cloud-infrastructure-engineering
product: thanos
tags: [thanos-sidecar, config-reloader, reloader-config-file, envsubst]
level: practitioner
status: docs-checked
description: "Use the sidecar reloader to watch Prometheus config and rule directories and reload on change."
sources: ["https://thanos.io/tip/components/sidecar.md/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Sidecar reloader

The sidecar can watch Prometheus configuration and trigger a reload, which requires Prometheus `--web.enable-lifecycle`.

- `--reloader.rule-dir=DIR` (repeatable) watches rule directories.
- `--reloader.config-file=FILE` watches a config file. Environment variables written as `$(VARIABLE)` are substituted, and the generated config is written to `--reloader.config-envsubst-file=OUT_FILE`.

Related flags and defaults:
- `--reloader.watch-interval=3m`: how often config and rules are re-read.
- `--reloader.retry-interval=5s`: retry cadence after a failed reload.
- `--reloader.method=http`: the reload method; the signal method matches the process by `--reloader.process-name` (default `prometheus`).

```
thanos sidecar \
  --reloader.config-file=/path/to/prometheus.yml.tmpl \
  --reloader.config-envsubst-file=/path/to/prometheus.yml \
  --reloader.rule-dir=/path/to/rules
```

## Checked

2026-11-03. Confirmed against the Thanos Sidecar page (components/sidecar.md) and the Thanos troubleshooting page: Store API over remote-read, 2h upload, block-duration requirement for upload, reloader flags, HTTP client config, upload-compacted, defaults. Fixed: the 2h fixed-block requirement applies to sidecar upload only. Removed: closing 'Verify' tips and other statements the page does not state.

Method: documentation only; no commands were run.
