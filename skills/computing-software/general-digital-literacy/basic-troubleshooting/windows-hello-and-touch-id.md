---
id: computing-software.general-digital-literacy.basic-troubleshooting.windows-hello-and-touch-id
name: windows-hello-and-touch-id
category: computing-software
field: general-digital-literacy
product: basic-troubleshooting
tags: [basic-troubleshooting, user-accounts, windows-hello, touch-id, face-id, biometric-sign-in, pin-sign-in, passkeys, fingerprint-reader]
level: intro
status: draft
description: "Set up Windows Hello (PIN, fingerprint, face) or Touch ID for faster, safer sign-in, and understand why a PIN or biometric beats a typed password on your device."
sources:
  - https://support.microsoft.com/en-us/windows
  - https://support.apple.com/guide/mac-help/welcome/mac
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# PIN, Windows Hello and Touch ID

**Goal:** sign in quickly and securely, and use the same unlock for passkeys and payments.

## Windows Hello
Settings › Accounts › **Sign-in options**:
- **PIN (Windows Hello)**: a device-only code; can include letters. Required before face/fingerprint.
- **Facial recognition** (needs an IR camera) or **Fingerprint recognition** (reader on keyboard or
  power button) › Set up › follow prompts. Add a second finger.
- Turn on *For improved security, only allow Windows Hello sign-in for Microsoft accounts on this
  device* to remove password sign-in.

## Touch ID / Face ID
- Mac: System Settings › **Touch ID & Password** › Add Fingerprint (up to 3 per user, 5 total); use
  for unlocking, Apple Pay, password autofill and app purchases.
- iPhone: Settings › Face ID & Passcode.

## Why a PIN is safer than a password here
The Windows Hello PIN is tied to that device's security chip (TPM): someone who learns it can't use
it from another computer, whereas your Microsoft account password works anywhere. Biometrics never
leave the device.

## Passkeys
Websites offering passkeys (Google, Microsoft, Apple, Amazon, banks) can use Windows Hello/Touch ID
to sign in with no password. Create one in the site's security settings.

## Gotchas
- Fingerprint fails with wet/dry skin or after cuts: enrol multiple fingers; the PIN/password always
  works as fallback.
- After major hardware changes or TPM resets you may need to set up the PIN again.

## Verify
- [ ] Lock (`Win+L`) and unlock with face/finger; fallback PIN works.
