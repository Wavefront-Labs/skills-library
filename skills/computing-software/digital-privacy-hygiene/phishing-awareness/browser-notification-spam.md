---
id: computing-software.digital-privacy-hygiene.phishing-awareness.browser-notification-spam
name: browser-notification-spam
category: computing-software
field: digital-privacy-hygiene
product: phishing-awareness
tags: [digital-privacy-hygiene, phishing-awareness, browser-notification-spam, tech-support-scam, malicious-extensions]
level: practitioner
status: draft
description: "Remove sites spamming fake virus alerts through browser push notifications in Chrome, Edge, Firefox, Safari and Android, and block future prompts."
sources:
  - "https://support.google.com/chrome/answer/3220216"
  - "https://support.mozilla.org/kb/push-notifications-firefox"
  - "https://support.apple.com/guide/safari/customize-website-notifications-sfri40734/mac"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Browser notification spam

**Goal:** stop the "Your PC is infected!" pop-ups that come from a website you once let send notifications.

## How it starts
A page says "Click **Allow** to confirm you're not a robot / to watch the video". That grants push notifications;
the site then sends fake alerts linking to scams, even when the site isn't open.

## Remove the permission
| Browser | Path |
|---|---|
| Chrome | Settings > Privacy and security > Site settings > Notifications > find site > Remove/Block |
| Edge | Settings > Cookies and site permissions > Notifications |
| Firefox | Settings > Privacy & Security > Permissions > Notifications > Settings > remove site |
| Safari (Mac) | Settings > Websites > Notifications > remove |
| Android Chrome | Chrome > Settings > Site settings > Notifications; or long-press the notification > settings |
| Windows | Settings > System > Notifications: turn off the browser's site notifications if needed |

Tip: the notification itself usually shows the sending site's domain; long-press/right-click it for a shortcut to
its settings.

## Prevent
- Set notifications default to **Don't allow sites to send notifications** (or Chrome "Use quieter messaging").
- Never click Allow on sites you don't know.

## Also check
Extensions (malicious ones also inject pop-ups) and that no "security" software was installed from those alerts.

## Gotchas
- These alerts imitate Windows Defender/McAfee styling; real antivirus alerts don't come from your browser with a
  website domain.
