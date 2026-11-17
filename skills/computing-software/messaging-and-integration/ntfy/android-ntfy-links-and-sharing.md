---
id: computing-software.messaging-and-integration.ntfy.android-ntfy-links-and-sharing
name: android-ntfy-links-and-sharing
category: computing-software
field: messaging-and-integration
product: ntfy
tags: [ntfy, android, deep-links, share, message-bar]
level: intro
status: docs-checked
description: "Use ntfy:// deep links, the share-to-topic feature and the in-app publish dialog on Android."
sources:
  - https://raw.githubusercontent.com/binwiederhier/ntfy/main/docs/subscribe/phone.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ntfy:// links, sharing and publishing from the app

## Deep links

`ntfy://<host>/<topic>` opens the topic and subscribes if needed; it is the equivalent of the HTTPS web URL.

- `?display=<name>` sets a display name.
- `?secure=false` uses HTTP instead of HTTPS.
- `https://<host>/<topic>/subscribe` links do not work for deep linking; use `ntfy://`.

```
ntfy://ntfy.example.com/mytopic?display=Alerts
```

## Publishing from the app

- The message bar is enabled by default (Settings, General, "Show message bar") at the bottom of the topic view. If disabled, a floating action button appears.
- The expand button opens the publish dialog: title, tags, priority, click URL, email forwarding, delayed delivery, attachments, Markdown and phone calls.

## Share to topic

Share files or text to a topic from any app that supports sharing. The app lists the last few topics you shared to.

## Checked

2026-11-04. Confirmed against the ntfy phone page (ntfy:// links, Publishing messages, Share to topic): link formats and parameters, message bar default, publish dialog contents, share list. Removed: the Verify step.
Method: documentation only; no commands were run.
