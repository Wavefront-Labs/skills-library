---
id: computing-software.cloud-infrastructure-engineering.alertmanager.slack-app-token-and-updates
name: slack-app-token-and-updates
category: computing-software
field: cloud-infrastructure-engineering
product: alertmanager
tags: [alertmanager, slack-config, bot-token, update-message]
level: advanced
status: docs-checked
description: "Using Slack bot tokens in Alertmanager: app_token, app_url, chat.postMessage, and update_message to edit existing messages; webhooks cannot update."
sources: ["https://prometheus.io/docs/alerting/latest/configuration/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Slack bot tokens and message updates

Besides incoming webhooks, Slack notifications can use Bot tokens.

For a webhook, `api_url` must be the webhook URL, or written to the file named by `api_url_file`.

For Bot tokens:
- `api_url` must be `https://slack.com/api/chat.postMessage`.
- The bot token is set as the authorization credentials in `http_config`.
- `channel` must contain either the name or the ID of the channel.

The newer fields also support app tokens: `app_token` / `app_token_file` (OAuth authentication) and `app_url` (required when using `app_token`). Either `api_url`/`api_url_file` OR `app_token`/`app_token_file` should be set, but not both. They default to the global `slack_app_token`, `slack_app_token_file` and `slack_app_url`.

```yaml
slack_configs:
- channel: C0123456789
  api_url: https://slack.com/api/chat.postMessage
  http_config:
    authorization:
      credentials: <bot-token>
  update_message: true
```

`update_message` (default `false`) updates existing Slack messages instead of creating new ones when alert state changes. Webhook URLs do not support updates.

Interactive buttons use `actions`, each with `text`, `type`, and either `url` or `name` plus `value`; optional `confirm` (with `text`, `dismiss_text`, `ok_text`, `title`) and `style`.

## Checked

2026-11-03. Confirmed against the Alertmanager Configuration page (prometheus.io/docs/alerting/latest/configuration): slack_config bot-token, app_token and update_message notes, action_config.

Method: documentation only; no commands were run.
