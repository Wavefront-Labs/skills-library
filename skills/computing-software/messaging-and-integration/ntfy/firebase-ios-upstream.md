---
id: computing-software.messaging-and-integration.ntfy.firebase-ios-upstream
name: firebase-ios-upstream
category: computing-software
field: messaging-and-integration
product: ntfy
tags: [ntfy, firebase, ios, upstream-base-url, apns]
level: advanced
status: docs-checked
description: "Give a self-hosted ntfy server instant iOS notifications with upstream-base-url, and when firebase-key-file applies."
sources:
  - https://raw.githubusercontent.com/binwiederhier/ntfy/main/docs/config.md
  - https://raw.githubusercontent.com/binwiederhier/ntfy/main/docs/known-issues.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Firebase and iOS instant notifications

## Firebase (FCM)

`firebase-key-file`: path to the Firebase Admin SDK JSON key (placed in `/etc/ntfy`). Firebase is optional and only works if you build your own Android .apk; the ntfy Android app uses it for ntfy.sh only and uses instant delivery for other hosts. Place the key in `/etc/ntfy`, set `firebase-key-file` and restart the server.

## iOS instant notifications

```yaml
base-url: "https://ntfy.example.com"
upstream-base-url: "https://ntfy.sh"
upstream-access-token: "tk_..."   # optional
```

If set, every incoming message publishes a `poll_request` to the upstream server, which forwards it to Firebase/APNS; the iOS app then polls your server for the content. Without it, delivery can take hours (typically no more than 20-30 minutes while you use the phone). The access token is optional, only if rate limits are exceeded or the upstream server is protected.

## Gotchas

- Set `upstream-base-url` to `https://ntfy.sh`, not your own hostname.
- `base-url` must exactly match the Default Server set in the iOS app.
- "New message" shown instead of content: the server sends the literal text `New message` to upstream; the iPhone shows it when it cannot reach your server. Check the network and turn on `log-level: debug` or `trace`.
- If iOS stops receiving, remove and re-add the subscription to force Firebase to re-subscribe.

## Checked

2026-11-04. Confirmed against the ntfy config page (Firebase (FCM), iOS instant notifications) and known issues page. Corrected: Firebase is optional and needs your own built apk; upstream-base-url is not strictly required, delivery is just slow without it. Removed: the Verify step.
Method: documentation only; no commands were run.
