---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.alertmanager-pagerduty-opsgenie-slack-receivers
name: alertmanager-pagerduty-opsgenie-slack-receivers
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [pagerduty-receiver, slack-receiver, opsgenie-receiver, alertmanager, receiver-integrations, notification-templates]
level: practitioner
status: docs-checked
description: "Configure Alertmanager PagerDuty (Events v2), Opsgenie and Slack receivers: key files, severity and priority templates, send_resolved defaults, bot-token Slack, global defaults."
sources: ["https://prometheus.io/docs/alerting/latest/configuration/#pagerduty_config", "https://prometheus.io/docs/alerting/latest/configuration/#slack_config", "https://prometheus.io/docs/alerting/latest/configuration/#opsgenie_config", "https://prometheus.io/docs/alerting/latest/notifications/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PagerDuty, Opsgenie and Slack receivers

```yaml
receivers:
  - name: payments-pager
    pagerduty_configs:
      - routing_key_file: /path/to/secrets/pd-payments   # Events API v2 integration key
        severity: '{{ if eq .CommonLabels.severity "page" }}critical{{ else }}warning{{ end }}'
        description: '{{ .CommonLabels.alertname }}: {{ .CommonAnnotations.summary }}'
        links:
          - {href: '{{ .CommonAnnotations.runbook_url }}', text: Runbook}
        send_resolved: true
  - name: platform-opsgenie
    opsgenie_configs:
      - api_key_file: /path/to/secrets/opsgenie
        priority: '{{ if eq .CommonLabels.severity "page" }}P1{{ else }}P3{{ end }}'
        tags: '{{ .CommonLabels.team }},{{ .CommonLabels.cluster }}'
  - name: payments-ticket
    slack_configs:
      - api_url_file: /path/to/secrets/slack-webhook
        channel: '#payments-alerts'
        send_resolved: true
        title: '[{{ .Status | toUpper }}] {{ .CommonLabels.alertname }}'
```

## Notes (from the configuration reference)
- PagerDuty: `routing_key` is the integration key for integration type `Events API v2`; `service_key` is the key for integration type `Prometheus`. They are mutually exclusive, and each has a `_file` twin (also mutually exclusive with it). `severity` is a template with default `error`; `links` take `href` and `text`.
- Opsgenie: `api_key` or `api_key_file` (conflict with each other); `priority` takes P1 to P5; `tags` is a comma separated list; `update_alerts` defaults to false (an existing alert is never updated, the new message only appears in the activity log).
- Slack: either an incoming webhook (`api_url` or `api_url_file` is the webhook URL) or a bot token (`api_url` set to `https://slack.com/api/chat.postMessage`, the token set as authorization credentials in `http_config`, and `channel` holding the channel name or ID; the `#` is optional). `channel` is a required field. Webhook URLs do not support `update_message`.
- Secrets can come from `*_file` fields instead of inline values.
- Global defaults exist for `slack_api_url`, `slack_api_url_file`, `pagerduty_url` and `opsgenie_api_url` (and `opsgenie_api_key[_file]`), and each receiver inherits them.
- Template data: `.Status` (firing if at least one alert is firing, otherwise resolved), `.CommonLabels`, `.CommonAnnotations`, `.Alerts.Firing`, `.Alerts.Resolved`, and functions such as `toUpper` (notification template reference).

## Gotchas
- `send_resolved` defaults to true for PagerDuty and Opsgenie but false for Slack; set it explicitly everywhere.
- To test a template without a real alert, `amtool template render --template.glob=... --template.text='{{ template "slack.default.markdown.v1" . }}'` (Alertmanager README).

## Verify
- [ ] Send a test alert with the severity your template keys on and confirm the resulting PagerDuty severity, Opsgenie priority and Slack message, and that the resolution notification arrives where `send_resolved` is true.

## Checked
Date: 2026-11-07. The Alertmanager configuration page is about 87 KB; I read the global defaults block, the full `<opsgenie_config>`, `<pagerduty_config>` (plus its image and link sub-blocks) and `<slack_config>` sections, and did not read the other receivers' sections (email, Jira, Telegram etc.). The notification template reference was read in full (Data, Alert, KV and string-function tables); the amtool template render command is from the Alertmanager README. Corrections: `service_key` is the integration key for the `Prometheus` integration type, not "legacy v1"; removed the "dedup key derived from group key" claim, the "channel may be ignored with webhooks" claim, the Slack mrkdwn runbook link text, the `amtool alert add` PagerDuty verify step and the Slack text template. The Slack snippet's `title` template uses only `.Status` and `toUpper`, which the template page confirms.
Method: documentation only; no commands were run.
