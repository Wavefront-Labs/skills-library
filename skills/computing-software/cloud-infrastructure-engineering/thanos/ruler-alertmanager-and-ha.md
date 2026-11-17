---
id: computing-software.cloud-infrastructure-engineering.thanos.ruler-alertmanager-and-ha
name: ruler-alertmanager-and-ha
category: computing-software
field: cloud-infrastructure-engineering
product: thanos
tags: [thanos-rule, alertmanager, alert-label-drop, ruler-ha]
level: advanced
status: docs-checked
description: "Configure Ruler external labels and alert relabelling so replicas deduplicate in Alertmanager."
sources: ["https://thanos.io/tip/components/rule.md/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Ruler HA, external labels and Alertmanager

Each Ruler replica needs identifying external labels via `--label`, otherwise running multiple replicas is impossible and blocks clash at compaction. Example pair: `cluster="eu1", replica="A"` and `cluster="eu1", replica="B"`.

Drop the replica label just before sending alerts so Alertmanager deduplicates them:

```
thanos rule \
  --label 'replica="A"' \
  --alert.label-drop replica \
  --alertmanagers.config-file am.yml
```

Advanced relabelling is available through `--alert.relabel-config` or `--alert.relabel-config-file`.

The docs advise using external labels different from those of the sources you alert on. Example: Ruler in cluster `mon1` alerting on Prometheus in `eu1`; if both use `cluster`, the alert's own origin label overwrites the monitored target's.

`--alertmanagers.config` / `-file` take several Alertmanagers, treated as one HA group; a send failure counts only if all instances fail.

**Must-alert metrics** (from another scraper):
- `thanos_alert_sender_alerts_dropped_total` above 0 means alerts are not reaching Alertmanager.
- `prometheus_rule_evaluation_failures_total` above 0 means evaluation gaps or ignored alerts.

## Checked

2026-11-03. Confirmed against the Thanos Ruler page (components/rule.md) and the Thanos tools page (rules-check): defaults, HA external labels and alert.label-drop, mon1/eu1 label example, partial_response_strategy default abort, stateless mode via remote write, rules-check behaviour and exit codes. Removed: closing 'Verify' tips and other statements the page does not state.

Method: documentation only; no commands were run.
