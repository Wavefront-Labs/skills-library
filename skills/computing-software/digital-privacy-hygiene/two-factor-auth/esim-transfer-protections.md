---
id: computing-software.digital-privacy-hygiene.two-factor-auth.esim-transfer-protections
name: esim-transfer-protections
category: computing-software
field: digital-privacy-hygiene
product: two-factor-auth
tags: [digital-privacy-hygiene, two-factor-auth, esim-transfer-security, sim-swap, carrier-number-lock]
level: practitioner
status: draft
description: "Protect your number against eSIM transfer and activation abuse: carrier SIM protection settings, quick-transfer flows and what to do on a surprise transfer."
sources:
  - "https://support.apple.com/en-us/118227"
  - "https://www.fcc.gov/consumers/guides/cell-phone-fraud"
  - "https://www.t-mobile.com/support/account/sim-protection"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# eSIM transfer protections

**Goal:** your number can't be moved to an attacker's eSIM by a convincing call, a stolen carrier login or a
quick-transfer trick.

## How eSIM moves happen
- **Device-to-device transfer** (e.g. iOS eSIM Quick Transfer, Android transfer): needs the old phone unlocked
  and nearby, sometimes a carrier confirmation.
- **Carrier app/website activation:** log in to the carrier account, request a new eSIM QR/code.
- **Store/phone support:** agent issues a new eSIM after "verifying" you.

## Lock it down
1. Carrier account: unique password, app/2FA, account PIN/passcode.
2. Turn on the carrier's **SIM protection / number lock / wireless account lock** feature so SIM or eSIM
   changes are blocked until you disable it from a verified session.
3. Port-out PIN set.
4. Phone screen lock and SIM PIN (so a stolen phone can't be used to move the eSIM).
5. Notifications for SIM changes to an email you monitor.

## Signs of a hijack
Sudden "SOS only"/no service while others have signal, carrier email about a new SIM or device, inability to
receive SMS codes.

## Response
Call the carrier from another phone, report unauthorized SIM change, regain the line, then secure accounts that
use SMS (see SIM-swap response).

## Gotchas
- An eSIM "QR code" emailed to you is the eSIM: whoever scans it first gets the line.
- Number lock may also block legitimate upgrades; disable briefly when you buy a new phone.
