---
id: computing-software.systems-network-administration.healthchecks.config-integration-settings
name: config-integration-settings
category: computing-software
field: systems-network-administration
product: healthchecks
tags: [healthchecks, integration-toggles, slack-oauth, telegram-bot, twilio-settings]
level: advanced
status: docs-checked
description: "Enable and configure self-hosted Healthchecks integrations: ENABLED toggles, Slack, Discord, Telegram, Twilio, Pushover, Matrix, Signal, GitHub, shell commands."
sources:
  - https://raw.githubusercontent.com/healthchecks/healthchecks/master/templates/docs/self_hosted_configuration.md
  - https://raw.githubusercontent.com/healthchecks/healthchecks/master/README.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
On/off toggles: `SLACK_ENABLED`, `MATTERMOST_ENABLED`, `MSTEAMS_ENABLED`, `OPSGENIE_ENABLED`, `PAGERTREE_ENABLED`, `PD_ENABLED`, `PROMETHEUS_ENABLED`, `ROCKETCHAT_ENABLED`, `SPIKE_ENABLED`, `VICTOROPS_ENABLED`, `WEBHOOKS_ENABLED`, `ZULIP_ENABLED` (default True each); `APPRISE_ENABLED` and `SHELL_ENABLED` default False.

`SHELL_ENABLED`: commands run with the permissions of the `sendalerts` process, so enable only for fully trusted users.

Per integration:
- Slack: `SLACK_CLIENT_ID` and `SLACK_CLIENT_SECRET` enable the OAuth2 flow instead of manual webhook URLs.
- Discord: `DISCORD_CLIENT_ID`, `DISCORD_CLIENT_SECRET`.
- Telegram: `TELEGRAM_BOT_NAME`, `TELEGRAM_TOKEN`; run `settelegramwebhook`; `SITE_ROOT` must be https.
- Pushover: `PUSHOVER_API_TOKEN`, `PUSHOVER_SUBSCRIPTION_URL`.
- PagerDuty: `PD_APP_ID` enables the Simple Install Flow.
- Matrix: `MATRIX_HOMESERVER`, `MATRIX_USER_ID`, `MATRIX_ACCESS_TOKEN`.
- Signal: `SIGNAL_CLI_SOCKET` (signal-cli as a JSON-RPC daemon).
- Twilio: `TWILIO_ACCOUNT`, `TWILIO_AUTH`, `TWILIO_FROM`, `TWILIO_MESSAGING_SERVICE_SID` (required for WhatsApp), `TWILIO_USE_WHATSAPP`, `WHATSAPP_UP_CONTENT_SID`, `WHATSAPP_DOWN_CONTENT_SID`.
- GitHub Issues: `GITHUB_CLIENT_ID`, `GITHUB_CLIENT_SECRET`, `GITHUB_PRIVATE_KEY`, `GITHUB_PUBLIC_LINK`.
- ntfy.sh: `NTFY_SH_TOKEN`. Trello: `TRELLO_APP_KEY`. Pushbullet: `PUSHBULLET_CLIENT_ID`, `PUSHBULLET_CLIENT_SECRET`.

Many secrets have `_FILE` variants.

## Checked

2026-11-04. Confirmed against the Healthchecks server configuration page: every ENABLED toggle and its default, SHELL_ENABLED behaviour under sendalerts, the per-integration variables, settelegramwebhook with an https SITE_ROOT, TWILIO_MESSAGING_SERVICE_SID required for WhatsApp, and the _FILE variants. Nothing removed.

Method: documentation only; no commands were run.
