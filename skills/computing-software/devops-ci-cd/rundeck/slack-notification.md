---
id: computing-software.devops-ci-cd.rundeck.slack-notification
name: slack-notification
category: computing-software
field: devops-ci-cd
product: rundeck
tags: [rundeck, slack-notification, incoming-webhook, freemarker-template, job-events]
level: practitioner
status: docs-checked
description: "Send Rundeck job events to a Slack channel with the Enterprise Slack notification plugin: split the incoming webhook URL into base URL and token, and set templates."
sources:
  - https://raw.githubusercontent.com/rundeck/docs/4.0.x/docs/manual/notifications/slack.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The Enterprise Slack plugin posts to a channel on: On Start, On Success, On Failure (failed or aborted), On Avg. Duration (exceeded average), On Retryable Failure.

Get the webhook in Slack: in your Slack app dashboard choose "Incoming Webhooks", turn "Activate Incoming Webhooks" on, then "Add new Webhook to Workspace" and pick the channel. The generated URL looks like `https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX`.

Split it into the plugin fields:
- Webhook Base URL: `https://hooks.slack.com/services`
- Webhook Token: everything after `services/`, here `T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX`
- Slack Channel: format `#slack-channel`
- Custom Template Path: directory for custom FreeMarker `.ftl` templates; blank means `${rdeck.base}/libext/templates`
- Custom Template: the `.ftl` file name; if not found in that path the plugin falls back to its built-in message format

Add it on the job's Notifications tab under the event you want.

## Checked

2026-11-04: the five events, webhook setup, the base URL and token split, channel format, template path default and template fallback confirmed against the Rundeck Slack Notification Plugin page. Removed an unsourced verify step.

Method: documentation only; no commands were run.
