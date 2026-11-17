---
id: computing-software.devops-ci-cd.semaphore-ui.notifications-overview
name: notifications-overview
category: computing-software
field: devops-ci-cd
product: semaphore-ui
tags: [notifications, alerts, server-channels, chat, email, semaphore-ui]
level: intro
status: docs-checked
description: "How Semaphore delivers task alerts, which channels exist, and the three checks that must all pass."
sources:
  - https://semaphoreui.com/docs/admin-guide/notifications
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Notifications overview

Goal: understand why an alert is or is not sent.

Two mechanisms: server channels (configured once in `config.json` or environment, shared by all projects) and project alerts (named destinations in a project's Alerts tab, bound to templates and schedules).

A server-channel message is sent only if all three hold:
1. The channel is configured on the server.
2. The project has Send alerts of this project to server channels turned on in its Alerts tab.
3. The template asks for it: project defaults send to server channels; a template with a custom alert list does not; templates can also suppress success or failure notifications.

Chat channels report success, failure and tasks waiting for confirmation; e-mail reports failures only.

Supported channels: E-mail (SMTP), Telegram, Slack, Microsoft Teams, Rocket.Chat, DingTalk, Gotify. Several can be active at once. E-mail and Telegram project alerts reuse the server's SMTP settings and bot token; a Gotify project alert without its own URL and token reuses the server pair.

Telegram supports a per-project chat via the Telegram Chat ID field.

Start small: configure one channel, enable the project switch, press Test all in the Alerts tab, then tune templates.

Verify: Test all delivers a message through every server channel and enabled project alert.

## Checked

2026-11-04: checked against the notifications page. Every claim is stated there.

Method: documentation only; no commands were run.
