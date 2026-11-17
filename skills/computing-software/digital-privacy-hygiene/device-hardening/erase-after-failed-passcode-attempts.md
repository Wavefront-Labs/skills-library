---
id: computing-software.digital-privacy-hygiene.device-hardening.erase-after-failed-passcode-attempts
name: erase-after-failed-passcode-attempts
category: computing-software
field: digital-privacy-hygiene
product: device-hardening
tags: [digital-privacy-hygiene, device-hardening, erase-after-failed-attempts, screen-lock, lost-device-response]
level: practitioner
status: draft
description: "Decide whether to enable erase-after-10-failed-attempts on iPhone and wipe options on Android, given escalating delays, backups and kids playing with phones."
sources:
  - "https://support.apple.com/guide/iphone/set-a-passcode-iph14a867ae/ios"
  - "https://support.apple.com/guide/security/passcodes-and-passwords-sec20230a10d/web"
  - "https://grapheneos.org/features"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Erase after failed passcode attempts

**Goal:** a thief with time can't brute-force a short passcode, without risking accidental wipes.

## iPhone
Settings > Face ID & Passcode > **Erase Data**: erases the device after 10 failed passcode attempts.
Even without it, iOS enforces escalating delays after repeated failures (minutes to an hour) and the Secure Enclave
limits attempts, so brute force is slow. Erase Data adds a hard stop.

## Android
- Stock Android has no user toggle; work profiles/MDM can set a max-failed-attempts wipe.
- Samsung: Lock screen > Secure lock settings > **Auto factory reset** (after 20 failed attempts).
- GrapheneOS: escalating throttling by the secure element and a **duress PIN/password** that wipes the device when
  entered.

## Decide
| Factor | Lean |
|---|---|
| Short (4-6 digit) passcode | Enable |
| Long alphanumeric passcode | Optional |
| Young kids play with your phone | Disable or teach; accidental wipes happen |
| Reliable recent backup | Enable safely |
| High-risk (journalist, activist) | Enable, plus long passcode |

## Prerequisites
Recent backup (iCloud/computer) and a tested restore; otherwise a wipe loses data.

## Gotchas
- Wiping removes evidence for lost-device tracking only if Activation Lock remains; Find My stays bound to your
  Apple Account after erase.
- Erase triggers on passcode attempts, not on Face ID failures.
