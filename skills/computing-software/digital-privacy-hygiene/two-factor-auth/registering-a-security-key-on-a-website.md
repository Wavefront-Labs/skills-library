---
id: computing-software.digital-privacy-hygiene.two-factor-auth.registering-a-security-key-on-a-website
name: registering-a-security-key-on-a-website
category: computing-software
field: digital-privacy-hygiene
product: two-factor-auth
tags: [digital-privacy-hygiene, two-factor-auth, security-key-registration, security-keys, backup-security-key]
level: practitioner
status: draft
description: "Register a hardware security key on a site step by step: PIN and touch prompts, naming, testing, adding a backup key and removing weaker methods."
sources:
  - "https://www.yubico.com/works-with-yubikey/catalog/"
  - "https://support.google.com/accounts/answer/6103523"
  - "https://pages.nist.gov/800-63-4/sp800-63b.html"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Registering a security key on a website

**Goal:** each important account has two working keys and you know which is which.

## Steps (generic)
1. Sign in; go to Security / Sign-in methods / Two-factor > **Add security key** (may be labelled passkey).
2. Browser dialog: choose **Security key** (not phone or this device) if both appear.
3. Insert key or tap NFC; enter the **FIDO2 PIN** if asked; touch the key when it blinks.
4. Name it: `YubiKey 5C - keyring` / `YubiKey NFC - safe`.
5. Repeat with the backup key right away.

## Test
Sign out, sign in with key 1. Sign out, sign in with key 2. Only then remove SMS.

## Passkey vs second factor
- Some sites store the key as a **passkey** (discoverable, username-less sign-in), using a resident slot.
- Others store it as a **second factor** after the password (non-discoverable). Both are phishing-resistant.
- YubiKey 5 series stores up to 100 discoverable credentials (older firmware 25); check with
  `ykman fido credentials list`.

## Record keeping
In the vault item notes: which keys are registered, date. Makes lost-key response quick.

## Gotchas
- Safari/iOS: NFC keys work by holding near the top of the phone; Lightning/USB-C keys plug in.
- Some sites allow only one key: put a passkey on a second key elsewhere or keep strong recovery codes.
- After a FIDO2 reset, every registration on that key is gone.
