---
id: computing-software.digital-privacy-hygiene.two-factor-auth.security-keys-for-apple-account
name: security-keys-for-apple-account
category: computing-software
field: digital-privacy-hygiene
product: two-factor-auth
tags: [digital-privacy-hygiene, two-factor-auth, apple-account-security-keys, account-hardening-programs, security-keys, apple-id, fido2, ios, macos, phishing-resistant-mfa]
level: practitioner
status: docs-checked
description: "Replace verification codes with FIDO security keys on your Apple Account (at least two), and know which devices, accounts and features stop working."
sources:
  - "https://support.apple.com/en-us/102637"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Security keys for Apple Account

**Goal:** stop Apple Account takeover via phished six-digit codes.

## What it does
With security keys on, signing in on a new device or the web needs your password plus
either a physical key or another trusted Apple device nearby (already signed in). These
are the only ways to sign in; verification codes are no longer used. If you lose all
trusted devices and keys you could be locked out permanently.

## Requirements
- At least two FIDO Certified keys that work with the Apple devices you use.
- iOS 16.3, iPadOS 16.3 or macOS Ventura 13.2 or later on all devices signed in.
- Two-factor authentication already on, and a modern web browser.
- Apple Watch, Apple TV and HomePod sign-in needs a supporting iPhone or iPad; iCloud for
  Windows needs version 15 or later.

## Connectors
NFC keys work only with iPhone; USB-C works with iPhone 15 or later and most Macs;
Lightning with iPhone 14 and earlier; USB-A with older Macs (or newer ones with an adapter).
Keys with both NFC and USB-C work with most devices.

## Setup
You must add and maintain at least two keys, up to six. iPhone or iPad: Settings > your
name > Sign-in & Security > Two-Factor Authentication > Security Keys > Add Security Keys.
Mac: System Settings > your name > Sign-in & Security > Two-Factor Authentication > Security
Keys > Set Up. A passcode or password must be set on the device. During setup you can stay
signed in on active devices or sign out of chosen ones; devices unused for more than 90
days are signed out and need compatible software plus a key to sign back in.

## When a key or trusted device is needed
Signing in on a new device or the web, resetting the password or unlocking the account,
and adding or removing security keys.

## Limitations
Older devices that cannot update, child accounts and Managed Apple Accounts are not
supported. An Apple Watch paired with a family member's iPhone is not supported. Apple
Vision Pro does not support keys during initial setup (a trusted iOS or iPadOS device can
help).

## Stop using keys
Settings > your name > Sign-in & Security > Two-Factor Authentication > Security Keys >
Remove All Security Keys; the account returns to six-digit codes.

## Store the keys
Keep keys in a safe place and in more than one place, for example one at home and one at
work; when travelling consider leaving one at home. Also see
`computing-software.digital-privacy-hygiene.two-factor-auth.apple-recovery-key-and-recovery-contact`.

## Verify
- [ ] Two keys are registered under Security Keys.
- [ ] A web sign-in asks for a key or a nearby trusted device.

## Checked
Checked 2026-11-08 against Apple Support 102637. Removed: the claim that resetting the
password accepts a "trusted device passcode", that older watches are the only exceptions
and that sign-in at a specific website prompts for a key.

Method: docs-only read of cited pages, 2026-11-08
