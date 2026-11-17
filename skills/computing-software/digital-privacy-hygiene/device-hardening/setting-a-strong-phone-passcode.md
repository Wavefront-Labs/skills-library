---
id: computing-software.digital-privacy-hygiene.device-hardening.setting-a-strong-phone-passcode
name: setting-a-strong-phone-passcode
category: computing-software
field: digital-privacy-hygiene
product: device-hardening
tags: [digital-privacy-hygiene, device-hardening, strong-passcode, screen-lock, ios, android, biometrics, secure-enclave, erase-data]
level: intro
status: draft
description: "Choose and set a phone passcode that resists guessing and shoulder-surfing: alphanumeric or long numeric, no patterns, with erase-after-failures and biometrics for convenience."
sources:
  - "https://support.apple.com/guide/security/welcome/web"
  - "https://ssd.eff.org/module/creating-strong-passwords"
  - "https://www.privacyguides.org/en/os/ios-overview/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Setting a strong phone passcode

**Goal:** the passcode is what the encryption ultimately rests on; make it expensive to guess and hard to watch.

## Pick the format
- **iPhone:** Settings > Face ID & Passcode > Change Passcode > **Passcode Options** > Custom Alphanumeric Code
  (best) or Custom Numeric Code (8+ digits).
- **Android:** Settings > Security & privacy > Device unlock > Screen lock > PIN or Password. Avoid **Pattern**:
  smudges and shoulder-surfing reveal it and the space of real-world patterns is small.
- Random digits, not dates, years, repeated or keyboard sequences; `123456`, `000000`, `121212` and birthdays
  top every leaked PIN list.
- Hardware throttling (Secure Enclave, Pixel Titan M2) slows guessing, but a 4-digit PIN is still exhaustible;
  6 random digits is a floor, 8-10 or alphanumeric is better for higher-risk users.

## Make biometrics carry the daily load
- Enable Face ID / fingerprint so a long passcode is typed rarely; that is what makes a long one bearable.
- Biometrics fall back to the passcode after restarts, 48 hours idle, or 5 failed attempts.

## Limit guessing and theft
- iPhone: **Erase Data** after 10 failed attempts (Face ID & Passcode screen). Have a backup first.
- Turn on **Stolen Device Protection** (iPhone) / **Theft protection** (Android) so a thief who watched you type
  the passcode still cannot change the Apple/Google account password without biometrics.
- Shield the screen when typing in public; thieves film bar patrons, then steal the phone.

## Gotchas
- Simple "4-digit" option still appears in Passcode Options; check older family phones.
- Never reuse the phone passcode as a password elsewhere.

## Verify
- [ ] Passcode is 8+ random digits or alphanumeric; not a pattern.
- [ ] Biometrics enrolled; Stolen Device Protection on.
