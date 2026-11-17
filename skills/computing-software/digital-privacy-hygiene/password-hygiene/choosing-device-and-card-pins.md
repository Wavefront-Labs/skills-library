---
id: computing-software.digital-privacy-hygiene.password-hygiene.choosing-device-and-card-pins
name: choosing-device-and-card-pins
category: computing-software
field: digital-privacy-hygiene
product: password-hygiene
tags: [digital-privacy-hygiene, password-hygiene, pin-selection, strong-passcode, password-strength]
level: practitioner
status: draft
description: "Choose phone, SIM, card and voicemail PINs that resist guessing: avoid the most common codes, dates and patterns, and prefer longer PINs."
sources:
  - "http://www.datagenetics.com/blog/september32012/"
  - "https://pages.nist.gov/800-63-4/sp800-63b.html"
  - "https://support.apple.com/guide/security/passcodes-and-passwords-sec20230a10d/web"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Choosing device and card PINs

**Goal:** PINs that survive a few guesses, which is all most attackers get.

## How bad common PINs are
Analyses of leaked 4-digit PINs (DataGenetics) found `1234` alone covers about 11%, and the top 20 PINs about a
quarter of all users. Years (`19xx`, `20xx`), birthdays (`MMDD`/`DDMM`), repeats (`1111`) and patterns on the keypad
(`2580` straight down) dominate.

## Rules
- **Random**, generated (dice, password manager), not chosen.
- Avoid: dates, years, repeats, sequences, keypad lines/shapes, the last digits of your phone number, house number.
- Longer where allowed: phones 6+ digits or alphanumeric; SIM PIN 6-8 digits; voicemail PIN 6+.
- Different PINs for phone, SIM, bank card, carrier account and voicemail.

## Where each matters
| PIN | Attack | Limit |
|---|---|---|
| Bank card | Stolen wallet, 3 tries | Avoid birthday on ID in same wallet |
| Phone passcode | Shoulder-surf + theft | iPhone delays escalate; optional erase after 10 |
| SIM PIN | Moving SIM to another phone | 3 tries then PUK |
| Voicemail | Remote access to voicemail (2FA calls) | Disable remote access if unused |
| Carrier account PIN | Social engineering at store | Different from all others |

## Store
In the password manager (custom hidden fields). For card PINs, don't write them on or near the card.

## Gotchas
- Watch for shoulder surfing in public; cover the keypad.
- A smudge pattern on a screen can reveal a short PIN; longer PINs and alphanumeric help.
