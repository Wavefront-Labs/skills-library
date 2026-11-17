---
id: computing-software.digital-privacy-hygiene.two-factor-auth.setting-a-sim-pin
name: setting-a-sim-pin
category: computing-software
field: digital-privacy-hygiene
product: two-factor-auth
tags: [digital-privacy-hygiene, two-factor-auth, sim-pin, puk, phone-number-security, sim-swap, phone-theft, esim, sms-2fa]
level: intro
status: draft
description: "Lock the physical SIM/eSIM with a PIN so a stolen phone's SIM can't be moved to another handset to receive your SMS codes; avoid the PUK lockout."
sources:
  - "https://support.apple.com/en-us/102594"
  - "https://support.google.com/android/answer/9116416"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Setting a SIM PIN

**Goal:** a thief who takes your phone (or just the SIM) can put the SIM in another
phone and receive your texts, including 2FA and password resets, even if your phone
is locked. A SIM PIN blocks that.

## Before you start
- Find your carrier's **default SIM PIN** (often `0000`, `1111` or `1234`; check the
  carrier's site or the SIM card holder). Guessing wrong 3 times locks the SIM.
- Find the **PUK** (on the SIM card holder or in your carrier account). 10 wrong PUK
  attempts permanently disables the SIM.

## iPhone
Settings > Cellular (Mobile Data) > [line] > **SIM PIN** > on > enter default PIN >
Change PIN to a new 4-8 digit PIN.

## Android
Settings > Security & privacy > More security settings > **SIM card lock** (wording
varies) > Lock SIM card > enter default > Change SIM PIN.

## After setting
- The PIN is required at every reboot and when the SIM is moved. Store it (and the PUK)
  in your password manager.
- eSIMs also support a PIN; set it the same way. eSIM swaps happen through the carrier,
  so pair with carrier account protection (port-out PIN/number lock).

## Gotchas
- Don't use the same digits as your phone passcode.
- A SIM PIN doesn't stop a **carrier-side** SIM swap (social engineering the store);
  that needs carrier account locks.
- Locked out: enter PUK from the carrier, then set a new PIN.

## Verify
- [ ] Reboot the phone: SIM PIN prompt appears before mobile service connects.
