---
id: computing-software.messaging-and-integration.ntfy.click-and-icon
name: click-and-icon
category: computing-software
field: messaging-and-integration
product: ntfy
tags: [ntfy, click, icon, x-click, x-icon]
level: intro
status: docs-checked
description: "Make an ntfy notification open a URL or app when tapped with X-Click, and set a custom icon with X-Icon (Android)."
sources:
  - https://raw.githubusercontent.com/binwiederhier/ntfy/main/docs/publish.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Click action and icons

## Click action

Header `X-Click` (alias `Click`). `http://` and `https://` URLs open the browser; other schemes open the matching app (`mailto:`, `geo:`, `ntfy://`, `twitter://`).

```
curl -H "Click: https://www.reddit.com/message/messages" -d "New messages" ntfy.sh/reddit_alerts
```

The publish page marks click actions as supported on Android, Apple and Firefox.

## Icons

Header or query parameter `X-Icon` (alias `Icon`) set to an image URL.

```
curl -H "Icon: https://example.com/icon.png" -d "Hi" ntfy.sh/mytopic
```

- Only JPEG and PNG are supported.
- Android only.
- The client downloads the icon unless it has a cached copy newer than 24 hours; icons stay cached until the notification is deleted.

## Checked

2026-11-04. Confirmed against the ntfy publish page (Click action, Icons, JSON field table): header names and aliases, URL schemes, JPEG and PNG only, Android only, 24-hour cache rule. Removed: a web-app browser claim and the Verify step.
Method: documentation only; no commands were run.
