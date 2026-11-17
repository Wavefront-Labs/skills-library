---
id: computing-software.digital-privacy-hygiene.vpn-tools.auditing-signal-linked-devices
name: auditing-signal-linked-devices
category: computing-software
field: digital-privacy-hygiene
product: vpn-tools
tags: [digital-privacy-hygiene, vpn-tools, signal-linked-devices, signal, signal-desktop, linked-device-phishing, qr-code-phishing, account-compromise]
level: intro
status: docs-checked
description: "Check Signal's linked devices list, unlink unknowns, and avoid malicious QR codes disguised as group invites that link an attacker's device to your account."
sources:
  - "https://ssd.eff.org/module/how-to-use-signal"
  - "https://cloud.google.com/blog/topics/threat-intelligence/russia-targeting-signal-messenger"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Auditing Signal linked devices

**Goal:** a linked Signal device (computer or tablet) receives your messages too. If an attacker links one, they
read your conversations going forward without compromising your phone.

## Check
- Android: tap your profile picture, then Linked Devices. iPhone: profile picture, Settings, Linked Devices.
- Look for devices you do not recognise or no longer use. To remove one, tap the three-dot icon next to it and
  choose Unlink.
- EFF notes linking requires approval with a PIN or biometric, so unauthorised linking is unlikely but not
  impossible, and you may forget a link to a shared device such as an iPad. Review the page occasionally.

## The QR attack
Google Threat Intelligence (published 19 February 2025) reported Russian-aligned actors abusing Signal's linked
devices feature. Because linking involves scanning a QR code, they crafted malicious QR codes that link the
victim's account to an actor-controlled Signal instance; future messages then reach both the victim and the actor
in real time, giving persistent eavesdropping without full-device compromise. The codes were frequently disguised
as Signal group invites, security alerts or device pairing instructions from the Signal website, and were also
embedded in phishing pages posing as specialised Ukrainian military applications.
- Treat any QR code or page presented as a group invite, security alert or software update, urging immediate
  action, with caution.
- Google says the latest Signal releases for Android and iOS include hardening against these campaigns; keep Signal
  updated.

## Verify
- [ ] The linked devices list contains only devices you currently use.

## Checked
Method: docs-checked 2026-11-09 against the EFF Surveillance Self-Defense "How to use Signal" section "Review Your Linked Devices" (read in full) and the Google Cloud Threat Intelligence post on Russia targeting Signal (linked-devices section and introduction read from the downloaded HTML). Dropped as unconfirmed: the WhatsApp equivalent, the rule to scan only a QR shown by your own Desktop, the group-invite-link behaviour, history-transfer notes, the unlinking-does-not-delete note and the monthly reminder. support.signal.org could not be read and was removed.
