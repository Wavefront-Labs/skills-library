---
id: computing-software.devops-ci-cd.rundeck.webhook-notification-plugin
name: webhook-notification-plugin
category: computing-software
field: devops-ci-cd
product: rundeck
tags: [rundeck, webhook-notification, sha256-digest, url-token-expansion, notification-headers]
level: advanced
status: docs-checked
description: "Use the built-in webhook job notification: payload formats, X-Rundeck-Notification headers, URL token expansion and the optional SHA-256 digest check."
sources:
  - https://raw.githubusercontent.com/rundeck/docs/4.0.x/docs/manual/notifications/webhooks.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
This job notification plugin POSTs to one or more URLs when a job succeeds or fails. The body is XML by default (a `<notification>` root with `trigger`, `executionId` and `status` attributes) or JSON if chosen: `{"trigger":"success","status":"succeeded","executionId":<id>,"execution":{...}}`.

Headers sent:
- `X-Rundeck-Notification-Trigger`: success or failure
- `X-Rundeck-Notification-Execution-ID`
- `X-Rundeck-Notification-Execution-Status`: succeeded, failed or aborted

Optional verification: set `rundeck.notification.webhookSecurityKey` and every notification also carries `X-RunDeck-Notification-SHA256-Digest`. The receiver recomputes a SHA-256 over the post URL, trigger, execution id and the secret key, hex encodes it, and compares.

URL token expansion: URLs may contain `${job.name}`, `${job.group}`, `${job.id}`, `${job.project}`, `${execution.id}`, `${execution.user}`, `${execution.status}` and `${notification.trigger}`:

```
http://server/callback?id=${execution.id}&status=${execution.status}&trigger=${notification.trigger}
```

## Checked

2026-11-04: payload formats, headers, SHA-256 digest property and receiver steps, and URL tokens confirmed against the Webhooks notification page. Removed the unsourced Verify line.
Method: documentation only; no commands were run.
