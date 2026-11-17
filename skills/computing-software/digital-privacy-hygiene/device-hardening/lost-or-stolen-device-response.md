---
id: computing-software.digital-privacy-hygiene.device-hardening.lost-or-stolen-device-response
name: lost-or-stolen-device-response
category: computing-software
field: digital-privacy-hygiene
product: device-hardening
tags: [digital-privacy-hygiene, device-hardening, lost-device-response, find-my, find-hub, remote-wipe, lost-mode, sim-swap, physical-security, phone-theft]
level: intro
status: draft
description: "First-hour response to a lost or stolen phone or laptop: locate and lock, suspend the SIM, protect accounts, decide when to wipe, and report the theft."
sources:
  - "https://support.apple.com/en-us/101593"
  - "https://support.google.com/android/answer/6160491"
  - "https://consumer.ftc.gov/articles/how-protect-your-phone-and-data-it"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Lost or stolen device response

**Goal:** limit what a thief can do with your device and the accounts on it.

## First hour (from another device)
1. **Locate and lock**:
   - iPhone/Mac: `icloud.com/find` > **Mark As Lost** (locks, shows a message, disables
     Apple Pay).
   - Android: `android.com/find` (Find Hub) > **Secure device**; or Remote Lock with
     your phone number.
   - Windows: account.microsoft.com/devices > Find my device > Lock.
2. **Call your carrier**: suspend the line / block the SIM (stops SMS codes reaching the
   thief) and ask for a SIM PIN lock note; get a replacement SIM later.
3. **Accounts**: change Apple/Google password if the passcode may have been seen; sign
   out the device from email, banking apps, password manager (remove device sessions);
   freeze cards in banking apps (Apple Pay/Google Pay tokens are removed by Lost Mode/wipe).
4. Messengers: WhatsApp re-registration on new SIM; Signal will deregister when you
   register elsewhere.

## Wipe or not
Erase remotely once you're sure you won't recover it (wiping ends location tracking).
With Activation Lock / Factory Reset Protection, the device stays tied to your account; don't
remove it from your account until wiped, and ignore texts "from Apple" asking you to
remove it (a common thief phishing trick).

## Report
Police report (needed for insurance), carrier blacklist by IMEI, employer IT for work data.

## Verify
- [ ] Device locked/marked lost; SIM suspended; key accounts' sessions removed.
