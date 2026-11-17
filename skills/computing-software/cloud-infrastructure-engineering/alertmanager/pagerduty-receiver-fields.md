---
id: computing-software.cloud-infrastructure-engineering.alertmanager.pagerduty-receiver-fields
name: pagerduty-receiver-fields
category: computing-software
field: cloud-infrastructure-engineering
product: alertmanager
tags: [alertmanager, pagerduty-config, routing-key, events-api-v2]
level: practitioner
status: docs-checked
description: "pagerduty_configs fields: routing_key versus service_key, severity default, details defaults, images, links, component, group, class, timeout."
sources: ["https://prometheus.io/docs/alerting/latest/configuration/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# pagerduty_configs

Alertmanager 0.11 and later uses PagerDuty's Events API v2.

```yaml
receivers:
- name: team-X-pager
  pagerduty_configs:
  - routing_key_file: /path/to/pd-key
    severity: critical
    component: '{{ .CommonLabels.job }}'
```

Fields:
- `send_resolved`: default `true`.
- Keys are mutually exclusive: `routing_key` / `routing_key_file` for integration type Events API v2, or `service_key` / `service_key_file` for integration type Prometheus. Both are template secrets.
- `url`: default `global.pagerduty_url`.
- `client` and `client_url`: default to `pagerduty.default.client` and `pagerduty.default.clientURL` templates.
- `description`: default `pagerduty.default.description` template.
- `severity`: default `error`.
- `source`: default is the `client` value.
- `details`: defaults to `firing`, `resolved` (both as `.Alerts.Firing`/`.Alerts.Resolved | toJSON`), `num_firing` and `num_resolved` (as `len`). Nested key/value pairs are accepted with Events API v2.
- `images`: list of `href`, `src`, `alt`. `links`: list of `href`, `text`.
- `component`, `group`, `class`: optional template strings.
- `timeout`: default `0s` (none); no effect if set above `group_interval`.

## Checked

2026-11-03. Confirmed against the Alertmanager Configuration page (prometheus.io/docs/alerting/latest/configuration): pagerduty_config fields and defaults.

Method: documentation only; no commands were run.
