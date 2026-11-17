---
id: computing-software.cloud-infrastructure-engineering.thanos.ruler-stateless-remote-write
name: ruler-stateless-remote-write
category: computing-software
field: cloud-infrastructure-engineering
product: thanos
tags: [thanos-rule, stateless-ruler, remote-write-config, wal-only]
level: sme
status: docs-checked
description: "Run a stateless Thanos Ruler that writes results by remote write instead of a local TSDB."
sources: ["https://thanos.io/tip/components/rule.md/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Stateless Ruler via remote write

A stateless Ruler gains near-unlimited horizontal scalability: it has no full TSDB, uses a WAL-only store (reusing the upstream Prometheus agent), and sends evaluation results to a remote store with remote write. It is compatible with older TSDB data.

Enable it by passing a Prometheus remote-write config with `--remote-write.config` (inline) or `--remote-write.config-file`:

```
thanos rule \
  --data-dir "/path/to/data" \
  --eval-interval "30s" \
  --rule-file "/path/to/rules/*.yaml" \
  --query "query.monitoring.svc:9090" \
  --remote-write.config-file rw.yaml
```

```yaml
remote_write:
- url: "http://receive.monitoring.svc:19291/api/v1/receive"
```

Supporting flags: `--restore-ignored-label` lists labels ignored when restoring alert state from remote storage (stateless only), and `--query.default-step` (1s) is used for range queries in stateless mode and alert state restoration.

In stateless mode the Ruler does not expose the Store API; if the remote store is Thanos Receive, query the rule results there.

## Checked

2026-11-03. Confirmed against the Thanos Ruler page (components/rule.md) and the Thanos tools page (rules-check): defaults, HA external labels and alert.label-drop, mon1/eu1 label example, partial_response_strategy default abort, stateless mode via remote write, rules-check behaviour and exit codes. Removed: closing 'Verify' tips and other statements the page does not state.

Method: documentation only; no commands were run.
