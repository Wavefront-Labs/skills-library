---
id: computing-software.general-digital-literacy.basic-troubleshooting.sim-esim-and-no-service
name: sim-esim-and-no-service
category: computing-software
field: general-digital-literacy
product: basic-troubleshooting
tags: [basic-troubleshooting, ts-mobile, esim, no-service, sim-card, sim-pin]
level: intro
status: draft
description: "Fix No Service and SOS only, insert or switch a SIM, add or transfer an eSIM, use dual SIM abroad, and recover from a locked SIM PIN with the PUK code."
sources:
  - https://support.apple.com/en-us/118227
  - https://support.apple.com/en-us/101593
  - https://support.google.com/android/answer/9475972
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# SIM, eSIM and No Service

## No Service / SOS only
1. Toggle **Airplane mode** on and off; restart.
2. Check the carrier's outage page (on Wi-Fi). Check you are in coverage.
3. Settings › Mobile/Cellular › the line is **on** and set as primary; data roaming on if abroad.
4. Physical SIM: power off, remove, check for damage, reinsert (right way up). Try it in another phone to see if the SIM or the phone is at fault.
5. Update carrier settings: iPhone Settings › General › About (prompt appears). Android: Settings › Network › reset mobile network settings.
6. Reset network settings (forgets Wi-Fi passwords): iPhone Settings › General › Transfer or Reset › Reset › Reset Network Settings.
7. Still nothing: the carrier may have suspended the line (unpaid bill, suspected SIM swap) → call them from another phone.

## eSIM
- A digital SIM; add via the carrier app, a **QR code** (Settings › Mobile › Add eSIM), or transfer from your old phone during setup.
- Deleting an eSIM removes it; you need the carrier to reissue. Don't delete it before a transfer is confirmed.
- **Travel eSIMs** (Airalo, Holafly, carrier travel passes) give local data abroad; keep your home line on for calls/2FA texts with data roaming off.

## SIM PIN and PUK
- SIM PIN protects the SIM if stolen. Three wrong PINs lock it; enter the **PUK** from the SIM card holder or the carrier's account/app. Ten wrong PUKs destroy the SIM.

## Verify
- [ ] Signal bars and carrier name show; a test call and text work; mobile data loads a page.
