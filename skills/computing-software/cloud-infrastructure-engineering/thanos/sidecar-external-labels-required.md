---
id: computing-software.cloud-infrastructure-engineering.thanos.sidecar-external-labels-required
name: sidecar-external-labels-required
category: computing-software
field: cloud-infrastructure-engineering
product: thanos
tags: [thanos-sidecar, external-labels, unique-labels, troubleshooting]
level: practitioner
status: docs-checked
description: "Fix the sidecar errors about no external labels or a refused connection to Prometheus."
sources: ["https://thanos.io/tip/operating/troubleshooting.md/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Sidecar: external labels and connection errors

**Connection refused.** A log line like `request flags against http://localhost:9090/api/v1/status/config ... connection refused` with `status=not-ready` means no server answers at the Prometheus URL. Make sure Prometheus is running and that `--prometheus.url` is correct before expecting the sidecar to become ready.

**Not identifying Prometheus.** The error `no external labels configured on Prometheus server, uniquely identifying external labels must be configured` appears when Prometheus has no external labels. Thanos needs unique, non-empty external labels for later processing. Add them to the Prometheus config:

```yaml
global:
  external_labels:
    cluster: eu1
    replica: 0
```

Labels must be globally unique per Prometheus and persistent over time: the compactor groups blocks by them, and Queriers use `replica` style labels for deduplication.

## Checked

2026-11-03. Confirmed against the Thanos Sidecar page (components/sidecar.md) and the Thanos troubleshooting page: Store API over remote-read, 2h upload, block-duration requirement for upload, reloader flags, HTTP client config, upload-compacted, defaults. Fixed: the 2h fixed-block requirement applies to sidecar upload only. Removed: closing 'Verify' tips and other statements the page does not state.

Method: documentation only; no commands were run.
