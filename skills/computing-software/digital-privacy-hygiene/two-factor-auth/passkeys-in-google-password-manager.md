---
id: computing-software.digital-privacy-hygiene.two-factor-auth.passkeys-in-google-password-manager
name: passkeys-in-google-password-manager
category: computing-software
field: digital-privacy-hygiene
product: two-factor-auth
tags: [digital-privacy-hygiene, two-factor-auth, google-password-manager-passkeys, passkey-enrollment, platform-passkeys, passkeys, android, chrome, google-password-manager-pin, google-account-passkey]
level: intro
status: draft
description: "Create and sync passkeys in Google Password Manager across Android and Chrome desktop, set its PIN, and separate it from a passkey for the Google account itself."
sources:
  - "https://support.google.com/accounts/answer/13548313"
  - "https://support.google.com/chrome/answer/13168025"
  - "https://security.googleblog.com/2024/09/passkeys-now-sync-across-devices.html"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Passkeys in Google Password Manager

**Goal:** use Google's passkey provider across Android phones and Chrome on any desktop.

## Two different things called "Google passkey"
1. A **passkey for your Google Account** (myaccount.google.com > Security > Passkeys
   and security keys): signs you into Google.
2. **Passkeys stored in Google Password Manager** for other websites (GitHub, eBay...).
Both can live in Google Password Manager; manage them in different places.

## Create
- Android 9+: site > Create passkey > choose Google Password Manager > screen lock.
- Chrome desktop (Windows, macOS, Linux, ChromeOS): Chrome offers to save passkeys to
  Google Password Manager when signed in with sync; first time you set a
  **Google Password Manager PIN** (6 digits or alphanumeric) used to unlock
  end-to-end encrypted passkeys on new devices.

## Sync and security
- Passkeys are end-to-end encrypted; a new device needs your screen lock from an
  existing Android device or the GPM PIN to join.
- Manage at `passwords.google.com` or `chrome://password-manager` > passkeys.

## Use
Username field suggestion or "Use passkey"; on other devices via QR/hybrid from the
Android phone.

## Gotchas
- Work profiles and multiple Google accounts: the passkey is saved to the account
  selected in the sheet; check before saving.
- Removing a Google account from a device doesn't delete passkeys from the cloud; delete
  in Password Manager and on the website.
- Uncertain: the PIN recovery behaviour differs by platform; record the PIN in your
  emergency kit.

## Verify
- [ ] Passkey created on Android signs in on Chrome desktop after entering the GPM PIN.
