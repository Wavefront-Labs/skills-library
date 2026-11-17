---
id: computing-software.cloud-infrastructure-engineering.alertmanager.mattermost-receiver-fields
name: mattermost-receiver-fields
category: computing-software
field: cloud-infrastructure-engineering
product: alertmanager
tags: [alertmanager, mattermost-config, webhook-url, props-card]
level: practitioner
status: docs-checked
description: "mattermost_configs fields: webhook_url, channel name, username, icon, Slack-style attachment fields, props card and priority settings."
sources: ["https://prometheus.io/docs/alerting/latest/configuration/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# mattermost_configs

Mattermost notifications are sent via the Mattermost webhook API.

```yaml
receivers:
- name: mm
  mattermost_configs:
  - webhook_url_file: /path/to/mattermost-webhook
    channel: town-square
    priority:
      priority: urgent
```

Fields:
- `send_resolved`: default `true`.
- `webhook_url` / `webhook_url_file`: mutually exclusive; global `mattermost_webhook_url` and `_file` exist.
- `channel`: override the channel; use the channel name, not the display name (`town-square`, not `Town Square`).
- `username`: overrides the poster name; defaults to the webhook's username, or `webhook` if none.
- `icon_url`; `icon_emoji` overrides both the profile picture and `icon_url`.
- Slack-compatible attachment fields: `fallback`, `color`, `title`, `title_link`, `text` (defaulting to `mattermost.default.*` templates), plus `pretext`, `author_name`, `author_link`, `author_icon`, `fields`, `thumb_url`, `footer`, `footer_icon`, `image_url`.
- `attachments` is deprecated and will be removed; use the top-level fields.
- `props.card`: Markdown text shown only in the right-hand panel after selecting the info icon.
- `priority.priority`: `urgent`, `important` or `standard`. `requested_ack` (default `false`) and `persistent_notifications` (default `false`; urgent only, repeats every five minutes) are Mattermost Enterprise only.

## Checked

2026-11-03. Confirmed against the Alertmanager Configuration page (prometheus.io/docs/alerting/latest/configuration): mattermost_config fields, props and priority config.

Method: documentation only; no commands were run.
