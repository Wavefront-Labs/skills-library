---
id: computing-software.general-digital-literacy.internet-navigation.hardware-security-keys
name: hardware-security-keys
category: computing-software
field: general-digital-literacy
product: internet-navigation
tags: [internet-navigation, in-authentication, security-key, yubikey, fido2, passkeys]
level: intro
status: docs-checked
description: "Use a FIDO2 hardware security key such as a YubiKey or Titan Key for phishing-resistant sign-in to Google, Microsoft, Apple and others, with a spare key and recovery plan."
sources:
  - https://support.google.com/accounts/answer/6103523
  - https://support.apple.com/en-us/102637
  - https://support.microsoft.com/en-us/accounts-billing/security/create-save-passkey
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Hardware security keys

A security key is a small USB-C/USB-A/NFC device that proves it's you by a touch. It only works on the **real** website, so it defeats phishing pages that steal codes.

## Who benefits
Journalists, activists, people with high-value accounts or crypto, admins, anyone targeted. Google offers its **Advanced Protection Program** for people at risk of targeted attacks.

## Buying
- FIDO Certified keys, for example **YubiKey 5** series, Google **Titan**, Feitian. Match your ports: Apple says keys with both NFC and USB-C work with most Apple devices. For a passkey on the key (sign in without a password) the key must support FIDO2; any FIDO1 or FIDO2 key can be a second step for Google.
- **Buy two**: one daily, one spare kept safe at home. Buy from the maker or an authorised seller.

## Set up
- **Google:** myaccount.google.com/signinoptions/passkeys › **Create a passkey** › *Use another device*; insert the key and enter its PIN or touch it. A newly added key may take up to 7 days to become available at sign-in.
- **Apple Account:** Settings › your name › Sign-In & Security › Two-Factor Authentication › **Security Keys** › Add Security Keys. You must add at least two keys (up to six) and need iOS 16.3, iPadOS 16.3 or macOS Ventura 13.2 or later on every signed-in device. Child and Managed Apple Accounts are not supported. Once enabled, a key or an already-trusted Apple device is the only way to sign in to a new device.
- **Microsoft (personal account):** account.live.com/proofs/manage (Advanced security options) › *Add a new way to sign in or verify* › *Face, Fingerprint, PIN, or Security Key*; the passkey can be saved on a physical security key.
- Other sites: look for security keys or passkeys in each site's security settings.
- Set a **PIN** on the key when asked (FIDO2 PIN, protects if stolen).

## Recovery
- Register **both** keys on every account. Keep **backup codes** in your password manager or printed.
- Losing all keys + codes may lock you out for good; Apple warns you could be locked out permanently if you lose all trusted devices and keys. Google may take 3-5 business days to recover an account with no other second step.

## Verify
- [ ] Signing in on a new browser asks you to touch the key; the spare key also works on each account.

## Checked

Checked 2026-10-27 against Apple Support 102637 (published 28 Apr 2026), Google Account Help 6103523 and 13548313, and Microsoft Support (create and save a passkey). Confirmed: Apple menu path, two to six keys, iOS 16.3 / macOS Ventura 13.2, child and managed accounts unsupported, key or trusted device as the only sign-in; Google passkey page, 7-day delay and 3-5 business day recovery; Microsoft Advanced security options path.

Method: documentation only; no commands were run.
