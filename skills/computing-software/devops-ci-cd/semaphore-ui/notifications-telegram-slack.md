---
id: computing-software.devops-ci-cd.semaphore-ui.notifications-telegram-slack
name: notifications-telegram-slack
category: computing-software
field: devops-ci-cd
product: semaphore-ui
tags: [telegram, slack, webhook, bot, notifications, semaphore-ui]
level: practitioner
status: docs-checked
description: "Set up Telegram bot and Slack incoming-webhook alerts via config keys or environment variables."
sources:
  - https://semaphoreui.com/docs/admin-guide/notifications/telegram
  - https://semaphoreui.com/docs/admin-guide/notifications/slack
  - https://semaphoreui.com/docs/admin-guide/notifications
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Telegram and Slack alerts

Goal: deliver task results to chat.

Telegram:
1. Message @BotFather with `/start`, create a bot and save the token.
2. Message your bot with `/start` so it can receive messages.
3. Message @RawDataBot and copy `id` from the `chat` object.
4. Test: `curl -X POST https://api.telegram.org/botYOUR_BOT_TOKEN/sendMessage -d chat_id=YOUR_CHAT_ID -d text="Test"`.
5. Configure:

```json
{ "telegram_alert": true, "telegram_token": "64********:AAG****", "telegram_chat": "<chat id>" }
```

A project can override the chat by setting Telegram Chat ID in its Alerts tab.

Slack:
1. At api.slack.com/apps create an app From Scratch, enable Incoming Webhooks, add a webhook to a channel and copy the URL.
2. Test: `curl -X POST -H 'Content-type: application/json' --data '{"text":"Hello"}' <webhook-url>`.
3. Configure:

```json
{ "slack_alert": true, "slack_url": "https://hooks.slack.com/services/XXX/YYY/ZZZ" }
```

Or `SEMAPHORE_SLACK_ALERT=True` and `SEMAPHORE_SLACK_URL=<url>`.

Gotchas:
- The bot token is secret. Environment variables keep sensitive values out of the configuration file.
- The project must have Send alerts of this project to server channels switched on.

Verify: Test all in the Alerts tab sends a message to the chat.

## Checked

2026-11-04: checked against the Telegram, Slack and notifications pages. Corrected the bot start wording and limited the secrecy gotcha to what the pages state.

Method: documentation only; no commands were run.
