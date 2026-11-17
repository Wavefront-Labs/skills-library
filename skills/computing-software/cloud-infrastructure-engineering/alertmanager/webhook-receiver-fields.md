---
id: computing-software.cloud-infrastructure-engineering.alertmanager.webhook-receiver-fields
name: webhook-receiver-fields
category: computing-software
field: cloud-infrastructure-engineering
product: alertmanager
tags: [alertmanager, webhook-config, max-alerts, custom-payload]
level: practitioner
status: docs-checked
description: "webhook_configs fields: url or url_file, max_alerts truncation, timeout, http_config and the advanced custom payload option."
sources: ["https://prometheus.io/docs/alerting/latest/configuration/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# webhook_configs

The webhook receiver is a generic receiver that sends HTTP POST requests to an endpoint.

```yaml
receivers:
- name: hook
  webhook_configs:
  - url_file: /path/to/webhook-url
    max_alerts: 50
    timeout: 10s
```

Fields:
- `send_resolved`: default `true`.
- `url` and `url_file`: mutually exclusive endpoint for HTTP POST requests.
- `http_config`: default `global.http_config`.
- `max_alerts`: maximum number of alerts in a single webhook message; alerts above are truncated. Default `0` includes all alerts.
- `timeout`: maximum time to wait for the request to complete before failing it and allowing a retry. Default `0s` means no timeout; no effect if higher than `group_interval`.
- `payload`: a map of string to template string that defines a custom payload.

The `payload` option is advanced. Alertmanager performs no validation of the result; the payload has to be valid JSON (the `toJson` function helps) and the Alertmanager team will not provide support for issues arising from it.

When `max_alerts` truncates, the JSON body reports how many were dropped in `truncatedAlerts`. The reference also points to a list of integrations that work with this receiver.

## Checked

2026-11-03. Confirmed against the Alertmanager Configuration page (prometheus.io/docs/alerting/latest/configuration): webhook_config fields, defaults, payload warning, truncatedAlerts. Removed: reference to another skill.

Method: documentation only; no commands were run.
