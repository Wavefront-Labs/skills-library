---
id: computing-software.digital-privacy-hygiene.two-factor-auth.carrier-sim-change-alerts
name: carrier-sim-change-alerts
category: computing-software
field: digital-privacy-hygiene
product: two-factor-auth
tags: [digital-privacy-hygiene, two-factor-auth, sim-change-alerts, sim-swap, phone-number-security]
level: practitioner
status: draft
description: "Turn on carrier notifications for SIM, eSIM, port and account changes, route them to email, and know what a real alert should trigger."
sources:
  - "https://www.fcc.gov/document/fcc-adopts-rules-protect-consumers-sim-swap-and-port-out-fraud"
  - "https://www.verizon.com/support/number-lock-faqs/"
  - "https://www.att.com/support/article/wireless/KM1051397/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Carrier SIM-change alerts

**Goal:** you hear about a SIM swap or port-out within minutes, even though the attacker now receives your texts.

## Why email matters
Alerts sent by SMS go to the hijacked number. FCC rules (2023) require carriers to notify customers of SIM
change and port-out requests; make sure notifications also reach an **email** you check.

## Setup
1. Carrier account > Profile/Notifications: add a current email; enable account-change, SIM change, port request
   and new device alerts.
2. Install the carrier app and enable push notifications on a **different** device (tablet) if possible.
3. Bank apps: many use SIM-swap signals; keep push notifications on.

## What triggers a response
- "Your SIM has been changed" / "eSIM activated" you didn't request.
- "Port-out request received".
- Phone shows no service or SOS only in a good-coverage area.

## Response
1. Call the carrier's fraud line from another phone, report it, ask them to reverse and add notes/locks.
2. From a trusted device: change email password, check email recovery settings, revoke sessions.
3. Remove SMS 2FA on financial accounts once the number is back.

## Gotchas
- Notifications are only useful if the email isn't on the same compromised chain (no SMS-only recovery).
- Prepaid/MVNO carriers may have fewer alert options; check and consider switching for your primary number.
