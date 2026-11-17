---
id: computing-software.digital-privacy-hygiene.two-factor-auth.passkeys-in-icloud-keychain
name: passkeys-in-icloud-keychain
category: computing-software
field: digital-privacy-hygiene
product: two-factor-auth
tags: [digital-privacy-hygiene, two-factor-auth, icloud-keychain-passkeys, passkey-enrollment, platform-passkeys, passkeys, apple-passwords-app, airdrop-passkey-sharing, shared-groups, apple-account]
level: intro
status: draft
description: "Create, use, share and remove passkeys in iCloud Keychain on iPhone, iPad and Mac, and understand what protects them (Apple Account, device passcode)."
sources:
  - "https://support.apple.com/en-us/102195"
  - "https://support.apple.com/guide/security/secure-keychain-syncing-sec0a319b35f/web"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Passkeys in iCloud Keychain

**Goal:** use Apple's built-in passkey provider safely.

## Requirements
- iOS/iPadOS 16+ or macOS Ventura+; iCloud Keychain on (Settings > [name] > iCloud >
  Passwords and Keychain); Apple Account with two-factor authentication.
- Passkeys sync end-to-end encrypted across your Apple devices; Apple can't read them.

## Create
Site's security settings > Create passkey > the system sheet "Save a passkey for
<account>?" > Continue (Face ID/Touch ID). If you use a third-party manager as well,
the sheet lets you choose where to save.

## Use
Sign-in page > username field or "Sign in with passkey" > Face ID. On a non-Apple
computer: choose "phone or tablet", scan the QR with the iPhone (see
`computing-software.digital-privacy-hygiene.password-managers.cross-device-passkey-sign-in-with-qr`).

## Manage
**Passwords app** (iOS 18+/macOS Sequoia; earlier: Settings > Passwords) > Passkeys tab:
view, delete, or move into a **Shared Group** to share with family. AirDrop sharing of
a single passkey is also possible.

## What protects them
- Your device passcode can authorise passkey use and, with the Apple Account password,
  can be used to restore iCloud Keychain on a new device. A thief who learned your
  passcode is a real risk: turn on **Stolen Device Protection** (iPhone).
- The Apple Account itself: consider security keys for it (see
  `computing-software.digital-privacy-hygiene.two-factor-auth.security-keys-for-apple-account`).

## Gotchas
- Deleting a passkey locally doesn't remove it from the website; remove it there too.
- Passkeys are not included in standard iCloud Keychain CSV exports; moving them uses
  newer credential-exchange features (iOS 26+); check current support.

## Verify
- [ ] Passkey created on iPhone works on your Mac without re-enrollment.
- [ ] Stolen Device Protection on.
