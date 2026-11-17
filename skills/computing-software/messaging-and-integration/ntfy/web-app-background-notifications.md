---
id: computing-software.messaging-and-integration.ntfy.web-app-background-notifications
name: web-app-background-notifications
category: computing-software
field: messaging-and-integration
product: ntfy
tags: [ntfy, web-app, background-notifications, web-push, browser-support]
level: practitioner
status: docs-checked
description: "Use the ntfy web app and its background (Web Push) notifications: when they work, browser support, one-week pause, and CORS for actions."
sources:
  - https://raw.githubusercontent.com/binwiederhier/ntfy/main/docs/subscribe/web.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Web app and background notifications

Subscribe by typing a topic and clicking "Subscribe". On ntfy.sh the app is at ntfy.sh/app. The browser must be allowed to show notifications.

## Background notifications

Enable in the "Settings" tab while subscribing.

- Off: an active ntfy tab must stay open (pinning it is suggested).
- On: uses the Web Push API; no active tab, but the browser may need to stay running. Works only with the server hosting the web app.
- They pause if the app goes unopened for more than a week; reopening resumes them, and you get a warning notification first.

## Browser support

- Chrome, Firefox, Edge, Opera on desktop: only while the browser is running.
- Safari desktop: running or not; needs Safari 16.1 and macOS 13 Ventura.
- Chrome and Firefox on Android: running or not.
- Safari on iOS: needs iOS 16.4 and the app added to the home screen.

## Gotchas

- Emoji tags and click actions work in all browsers; view and HTTP actions and images display only in Chrome, Edge and Opera.
- HTTP actions use fetch and need CORS (`Access-Control-Allow-Origin` of the ntfy origin or `*`).
- Installed web apps cannot turn background notifications off; mute topics instead.
- Self-hosted: configure Web Push (see web-push-config).

## Checked

2026-11-04. Confirmed against the ntfy web app page (Background notifications, browser support table, one-week pause, CORS for HTTP actions). Removed: the Verify step.
Method: documentation only; no commands were run.
