---
id: computing-software.digital-privacy-hygiene.vpn-tools.signal-usernames-and-phone-number-privacy
name: signal-usernames-and-phone-number-privacy
category: computing-software
field: digital-privacy-hygiene
product: vpn-tools
tags: [digital-privacy-hygiene, vpn-tools, signal-username, signal, signal-messenger, phone-number-privacy, who-can-find-me, username-link, qr-code]
level: intro
status: draft
description: "Share a Signal username instead of your phone number, set who can see and find you by number, and rotate or delete a username link that spread too far."
sources:
  - "https://support.signal.org/hc/en-us/articles/6712070553754-Phone-Number-Privacy-and-Usernames"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Signal usernames and phone number privacy

**Goal:** talk to new people (a group, a marketplace contact, a source) without
handing them your phone number.

## Set a username
Settings > Profile > **Username**: name plus 2+ digits (e.g. `river.07`), changeable later.
Share as text, a **QR code** or a **username link** (Profile > QR code or link).

## Phone number settings (Settings > Privacy > Phone number)
- **Who can see my number**: Nobody. Contacts who already have your number in their
  address book still see it.
- **Who can find me by number**: Everybody (default) or **Nobody**. With Nobody, people
  can't start a chat by typing your number; only via your username.

## Rotating
If a username or link has spread too far, change the username or **reset** the link /
QR (old one stops working). Existing conversations continue.

## Gotchas
- Your number is still registered with Signal and used for account recovery and
  Registration Lock; this hides it from **other users**, not from Signal's server.
- Groups: members see your profile name, not your number (if "Nobody").
- Pick a username that isn't your handle elsewhere if you want unlinkability.

## Verify
- [ ] From another account, search your number: not found (if set to Nobody).
- [ ] Username link opens a chat with you.
