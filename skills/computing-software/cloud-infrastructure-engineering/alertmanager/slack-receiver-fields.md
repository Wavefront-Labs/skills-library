---
id: computing-software.cloud-infrastructure-engineering.alertmanager.slack-receiver-fields
name: slack-receiver-fields
category: computing-software
field: cloud-infrastructure-engineering
product: alertmanager
tags: [alertmanager, slack-config, attachments, webhook-url]
level: practitioner
status: docs-checked
description: "Core slack_configs fields in Alertmanager: webhook api_url, channel, title, text, color, fields, footer, short_fields, mrkdwn_in and defaults."
sources: ["https://prometheus.io/docs/alerting/latest/configuration/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# slack_configs

Slack notifications use incoming webhooks or bot tokens, and the notification contains an attachment.

```yaml
receivers:
- name: slack-notifications
  slack_configs:
  - channel: '#alerts'
    api_url_file: /path/to/slack-webhook-url
    send_resolved: true
    title: '{{ template "slack.default.title" . }}'
```

Fields and defaults:
- `send_resolved`: default `false`.
- `api_url` (default `global.slack_api_url`) and `api_url_file` (default `global.slack_api_url_file`) for webhooks.
- `channel`: required; channel or user to send to.
- `username`, `icon_emoji`, `icon_url`: default to `slack.default.*` templates. `link_names`: default `false`.
- `message_text`: if set, sent as the top-level `text` field in the Slack payload; useful for simple notifications or Slack Workflow Webhooks.
- Attachment fields: `callback_id`, `color`, `fallback`, `fields`, `footer`, `pretext`, `text`, `title`, `title_link`, `image_url`, `thumb_url`, `actions`, each defaulting to a `slack.default.*` template where one exists.
- `mrkdwn_in`: default `["fallback", "pretext", "text"]`.
- `short_fields`: default `false`; a field's own `short` defaults to it.
- `timeout`: default `0s` (no timeout); no effect if higher than `group_interval`.

A `fields` entry needs `title` and `value`.

## Checked

2026-11-03. Confirmed against the Alertmanager Configuration page (prometheus.io/docs/alerting/latest/configuration): slack_config fields and defaults.

Method: documentation only; no commands were run.
