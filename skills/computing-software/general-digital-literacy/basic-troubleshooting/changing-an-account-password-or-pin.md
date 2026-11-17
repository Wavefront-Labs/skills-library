---
id: computing-software.general-digital-literacy.basic-troubleshooting.changing-an-account-password-or-pin
name: changing-an-account-password-or-pin
category: computing-software
field: general-digital-literacy
product: basic-troubleshooting
tags: [basic-troubleshooting, ts-accounts-signin, change-password, windows-hello-pin, mac-login-password]
level: intro
status: draft
description: "Change the sign-in password or PIN for a Windows, Microsoft, Mac or Chromebook account, understand which one you're changing, and avoid locking yourself out of encrypted data."
sources:
  - https://support.microsoft.com/en-us/windows
  - https://support.apple.com/guide/mac-help/welcome/mac
  - https://support.microsoft.com/en-us/account-billing
  - https://support.google.com/accounts
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Change the account password or PIN

## Windows
- Know your account type (Settings > Accounts > Your info): **Microsoft account** (email) or **local account**.
- **PIN** (Windows Hello): Settings > Accounts > Sign-in options > **PIN** > *Change PIN*. A PIN works only on that device.
- Microsoft account password: change at account.microsoft.com > Security > *Change password*; the PC picks it up next online sign-in (connect to the internet).
- Local account: Ctrl+Alt+Del > **Change a password**, or Settings > Sign-in options > Password > *Change*.
- Work/school accounts: Ctrl+Alt+Del > *Change a password* or your organisation's password portal.

## Mac
- System Settings > **Users & Groups** > (i) beside your user > **Change Password** (or Touch ID & Password > *Change*).
- The login keychain password updates automatically when changed this way. If reset another way, you'll be asked to update or create a new keychain.

## Chromebook
- Sign-in uses the Google account password: change at myaccount.google.com > Security. Device PIN: Settings > Security and privacy > Lock screen.

## Phone
- iPhone: Settings > Face ID & Passcode > *Change Passcode*. Android: Settings > Security > *Screen lock*.

## Before you change
- Write down the BitLocker/FileVault recovery key location (Microsoft account devices: aka.ms/myrecoverykey).
- Use a passphrase you can type; store it in a password manager.
- Admin-forced resets on shared PCs can lose access to encrypted files (EFS) and saved passwords.

## Verify
- [ ] Lock the screen and sign in with the new password/PIN before closing any notes.
