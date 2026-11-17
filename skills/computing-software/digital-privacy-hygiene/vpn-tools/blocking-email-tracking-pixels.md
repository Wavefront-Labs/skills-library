---
id: computing-software.digital-privacy-hygiene.vpn-tools.blocking-email-tracking-pixels
name: blocking-email-tracking-pixels
category: computing-software
field: digital-privacy-hygiene
product: vpn-tools
tags: [digital-privacy-hygiene, vpn-tools, email-tracking-pixels, email-privacy, remote-images, mail-privacy-protection, read-receipts, link-tracking, thunderbird, gmail-image-proxy]
level: intro
status: draft
description: "Stop marketing and phishing emails learning when, where and on what device you opened them: block remote images, use image proxies, and strip link trackers."
sources:
  - "https://www.privacyguides.org/en/basics/email-security/"
  - "https://support.apple.com/guide/iphone/use-mail-privacy-protection-iphf084865c7/ios"
  - "https://support.mozilla.org/en-US/kb/remote-content-in-messages"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Blocking email tracking pixels

**Goal:** a 1x1 remote image tells the sender you opened the mail, when, your IP
(approximate location) and client. Phishers use it to confirm live targets.

## Per client
| Client | Setting |
|---|---|
| Apple Mail (iOS/macOS) | Settings > Apps > Mail > Privacy Protection > **Protect Mail Activity** (preloads via proxy, hides IP and open time); or "Block All Remote Content" |
| Gmail web/app | Images are proxied by Google (hides IP, not the open event); Settings > General > Images > **Ask before displaying external images** |
| Outlook | File > Options > Trust Center > Automatic Download: don't download pictures automatically (desktop); Outlook.com settings similar |
| Thunderbird | Remote content blocked by default; allow per sender only |
| Proton / Tuta | Remote content blocked or proxied by default; check settings |

## Link tracking
Marketing links go through redirectors that log clicks. Options: uBlock Origin's URL
tracking protection list / ClearURLs-like features, NextDNS blocking of common mail
click-tracking domains (may break unsubscribe links), or hovering and visiting the clean
URL directly.

## Habits
- Don't click "unsubscribe" in obvious spam; it confirms your address. Mark as spam.
- Disable read receipts in clients that send them.

## Verify
- [ ] Send yourself an email with a remote image from a test service (e.g. an email
      tracking test site); no open is recorded, or IP is the proxy's.
