---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.alertmanager-receivers-and-webhooks
name: alertmanager-receivers-and-webhooks
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [alertmanager, receiver-integrations, msteams-receiver, telegram-receiver, sns-receiver, discord, webex, webhook-receiver, custom-webhook-payload]
level: practitioner
status: verified
description: "Configure Alertmanager receivers beyond Slack/PagerDuty (msteamsv2, Telegram, SNS, Discord, Webex) and build a webhook receiver that handles the JSON payload correctly."
sources: ["https://prometheus.io/docs/alerting/latest/configuration/#receiver-integration-settings", "https://prometheus.io/docs/alerting/latest/configuration/#webhook_config"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Alertmanager receivers and webhooks

```yaml
receivers:
  - name: teams
    msteamsv2_configs:                     # Workflows/Power Automate URL; msteams_configs is for legacy connectors
      - webhook_url_file: /etc/am/secrets/teams-url
        send_resolved: true
  - name: telegram
    telegram_configs:
      - bot_token_file: /etc/am/secrets/tg-token
        chat_id: -1001234567890
        parse_mode: HTML
  - name: sns
    sns_configs:
      - topic_arn: arn:aws:sns:eu-west-1:123456789012:alerts
        sigv4: {region: eu-west-1}         # IRSA / instance role
        subject: '{{ template "__subject" . }}'
  - name: discord
    discord_configs: [{webhook_url_file: /etc/am/secrets/discord}]
  - name: webex
    webex_configs:
      - room_id: <room>
        http_config: {authorization: {credentials_file: /etc/am/secrets/webex-token}}
  - name: ticketing
    webhook_configs:
      - url: http://alert-bridge.ops.svc:8080/alertmanager
        send_resolved: true
        max_alerts: 50                     # truncate huge groups; truncatedAlerts reports how many dropped
        http_config: {authorization: {credentials_file: /etc/am/secrets/bridge-token}}
```
Use `*_file` fields so secrets live in mounted files, not in the config Secret.

## Webhook payload (version 4)
```json
{"version":"4","groupKey":"{}:{alertname=\"X\"}","truncatedAlerts":0,"status":"firing",
 "receiver":"ticketing","groupLabels":{"alertname":"X"},"commonLabels":{...},"commonAnnotations":{...},
 "externalURL":"http://am:9093",
 "alerts":[{"status":"firing","labels":{...},"annotations":{...},"startsAt":"...","endsAt":"0001-01-01T00:00:00Z",
            "generatorURL":"...","fingerprint":"a1b2c3"}]}
```
Alertmanager 0.34.1 also sends `notification_reason` (for example `first notification`) and `routeLabels`.
Receiver rules:
- Idempotent on `fingerprint` (+ `startsAt`): the same group is re-sent every `repeat_interval` and from every
  HA Alertmanager peer if dedup fails.
- Return 2xx quickly; Alertmanager retries failed deliveries with backoff. With a closed port it logged `Notify attempt failed, will retry later` and, on give-up, `notify retry canceled after N attempts` (0.34.1).
- A group carries many alerts; resolved ones appear with `status: resolved` in the same list.
- Custom body: since Alertmanager 0.32.0 `webhook_configs[].payload` (a map of strings, each a Go template) replaces the default body; the result must be valid JSON (`toJson` helps) and the project gives no support for it. On 0.34.1 `payload: {st: '{{ .Status }}'}` sent `{"st":"firing"}`. On older versions transform the body in the bridge.

## Verify
- [ ] `amtool check-config alertmanager.yml` passes.
- [ ] Test alert via `amtool alert add test severity=info` reaches each receiver.
- [ ] `alertmanager_notifications_failed_total` by integration stays 0.
