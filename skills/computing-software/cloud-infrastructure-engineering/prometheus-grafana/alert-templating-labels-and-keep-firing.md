---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.alert-templating-labels-and-keep-firing
name: alert-templating-labels-and-keep-firing
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [prometheus, alerting-rules, alert-annotation-templating, labels-value-templating, severity-labels, alert-label-conventions, keep-firing-for-usage, flapping-suppression, runbook-url-annotation]
level: practitioner
status: verified
description: "Write alerting rules people can act on: annotation templates with $labels/$value/humanize, severity and ownership label conventions, and keep_firing_for against flapping."
sources: ["https://prometheus.io/docs/prometheus/latest/configuration/alerting_rules/", "https://prometheus.io/docs/prometheus/latest/configuration/template_reference/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Alert templating, label conventions and keep_firing_for

```yaml
- alert: DiskWillFillIn4Hours
  expr: |
    predict_linear(node_filesystem_avail_bytes{fstype!~"tmpfs|overlay"}[6h], 4*3600) < 0
    and node_filesystem_avail_bytes / node_filesystem_size_bytes < 0.2
  for: 15m
  keep_firing_for: 10m
  labels:
    severity: page            # page | ticket | info  (routing key, not "critical/warning" soup)
    team: platform            # owner: Alertmanager routes on it
  annotations:
    summary: "{{ $labels.instance }} {{ $labels.mountpoint }} fills within 4h"
    description: >-
      {{ $labels.mountpoint }} on {{ $labels.instance }} has
      {{ with printf `node_filesystem_avail_bytes{instance="%s",mountpoint="%s"}` $labels.instance $labels.mountpoint | query }}{{ . | first | value | humanize1024 }}B{{ end }} free.
      Cluster {{ $externalLabels.cluster }}.
    runbook_url: https://runbooks.example.com/disk-fill
    dashboard: https://grafana.example.com/d/node?var-instance={{ $labels.instance }}
```

## Templating
- `$labels.<name>`, `$value` (float of the alert expression), `$externalLabels.<name>`.
- Functions: `humanize` (1234.5 -> 1.234k), `humanize1024` (1536 -> `1.5ki`; append your own `B`), `humanizeDuration` (3600 -> `1h 0m 0s`), `humanizePercentage` (0.05 -> 5%),
  `printf "%.2f"`, `query` to fetch extra context, `title`, `toUpper`, `reReplaceAll`.
- Don't template **labels** with `$value`: a changing label creates a new alert each evaluation (flapping,
  re-notification; tested: with `for: 3m` such an alert never left pending). Values belong in annotations.

## Label conventions
- `severity`: what to do (page now / ticket / info), consistent across all teams.
- `team` or `owner`: who; derive from metric labels where possible (`team: "{{ $labels.namespace_owner }}"`
  is fine because it's stable).
- Keep alert identity stable: label set = alertname + labels; extra labels from the expression (pod) stay.

## keep_firing_for (2.42+)
After the expression stops returning, the alert keeps firing for this duration. Stops resolve/re-fire
flapping caused by a metric hovering at the threshold or brief scrape gaps. Typical 5-15 min. It delays the
"resolved" notification by that much (tested with `for: 15m` and `keep_firing_for: 10m`: the alert was still firing 5 minutes after its series vanished and gone after 10).

## Verify
- [ ] `promtool test rules` checks rendered annotations.
- [ ] Every alert has `severity`, `team`, `summary`, `runbook_url`.
- [ ] Flappy alerts (resolve/fire > 3x/hour in Alertmanager history) have `keep_firing_for`.
