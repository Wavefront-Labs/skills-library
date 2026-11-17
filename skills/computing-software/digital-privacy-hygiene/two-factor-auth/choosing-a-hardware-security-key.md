---
id: computing-software.digital-privacy-hygiene.two-factor-auth.choosing-a-hardware-security-key
name: choosing-a-hardware-security-key
category: computing-software
field: digital-privacy-hygiene
product: two-factor-auth
tags: [digital-privacy-hygiene, two-factor-auth, security-key-selection, security-keys, yubikey, google-titan, nitrokey, fido2, u2f, nfc-security-key, usb-c, discoverable-credentials, fips]
level: intro
status: draft
description: "Pick a hardware security key by connector (USB-A/C, Lightning, NFC), FIDO2 vs U2F-only, passkey slot count, extra applets (OATH, PIV, OpenPGP) and buy two."
sources:
  - "https://www.privacyguides.org/en/security-keys/"
  - "https://www.yubico.com/products/"
  - "https://fidoalliance.org/certification/fido-certified-products/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Choosing a hardware security key

**Goal:** buy the right pair of keys once.

## Decision points
1. **Connectors**: match every device you log in on. USB-C + NFC covers modern laptops
   and phones (tap on the back of iPhone/Android). Keep a USB-A or Lightning variant
   only if you still have such devices.
2. **FIDO2 (CTAP2) not just U2F**: FIDO2 supports passkeys (discoverable credentials)
   and PIN. U2F-only keys (older, cheapest) work only as a second factor after a password.
3. **Passkey slots**: discoverable credentials are stored on the key and capacity is
   limited (YubiKey 5 firmware before 5.7: 25; 5.7+: 100; others vary). Non-discoverable
   (2FA-style) registrations are unlimited.
4. **Extra applets** if you want them: OATH TOTP/HOTP (Yubico Authenticator), PIV smart
   card, OpenPGP, HMAC challenge-response (KeePassXC). YubiKey 5 has all; Security Key
   series is FIDO-only.
5. **Open firmware/source** preference: Nitrokey, SoloKeys (FIDO) publish firmware;
   YubiKey firmware is closed and not updatable (a flaw means replacing the key).
6. **Certification**: FIDO Certified; FIPS variants only if an employer requires it.

## Buy two (or three)
Register a **backup key** on every account at the same time as the primary (see
`computing-software.digital-privacy-hygiene.two-factor-auth.registering-a-backup-security-key`).
Keep the backup at home or off-site; carry the primary on your keyring.

## Where to buy
Directly from the manufacturer or an authorised reseller; avoid marketplace sellers
(tampered/used keys are a supply-chain risk).

## Gotchas
- Biometric keys (YubiKey Bio) can't be backed up any differently; still need two.
- Some phones' NFC antennas are finicky; test tap location.

## Verify
- [ ] Key works on every computer and phone you use (test at webauthn.io).
- [ ] Two keys purchased and labelled.
