---
id: computing-software.general-digital-literacy.basic-troubleshooting.forgot-computer-password
name: forgot-computer-password
category: computing-software
field: general-digital-literacy
product: basic-troubleshooting
tags: [basic-troubleshooting, user-accounts, forgot-computer-password, reset-pin, microsoft-account-password, local-account-recovery, mac-login-password, apple-id-reset, bitlocker-recovery-key]
level: intro
status: draft
description: "Get back into a Windows or Mac you can't sign into: reset a Microsoft account password or PIN, local account security questions, Mac Apple Account reset, BitLocker key."
sources:
  - https://support.microsoft.com/en-us/windows
  - https://support.apple.com/guide/mac-help/welcome/mac
  - https://account.live.com/password/reset
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Forgot computer password

**Goal:** regain access without losing your files.

## Windows 11
- **PIN forgotten:** sign-in screen › *I forgot my PIN* › verify your Microsoft account › set a new PIN.
- **Microsoft account** (sign-in shows an email address): *I forgot my password* on the sign-in
  screen, or reset from another device at **account.live.com/password/reset**. Use the new password
  (the PC must be online).
- **Local account** (shows just a name): *Reset password* link appears after a wrong attempt;
  answer your security questions. Without them, another admin account on the PC can reset it
  (Settings › Accounts › Other users is not enough: use Computer Management › Local Users, or
  `net user <name> *` in an admin Terminal). Otherwise the only route is a reset/reinstall.
- **BitLocker recovery screen** after resets or hardware changes: the 48-digit key is at
  **aka.ms/myrecoverykey** (sign in with the Microsoft account), with your IT department, or on a
  printout you saved.

## Mac
After three wrong tries, the login window offers to reset using your **Apple Account**, or with the
FileVault **recovery key**. Another admin user on the Mac can reset it in System Settings › Users &
Groups. From macOS Recovery: Utilities › Terminal › `resetpassword`.

## Prevent
- Store the computer password, Microsoft/Apple account password and recovery keys in a password
  manager (on another device) or printed in a safe place.
- Keep a second admin account for the household.

## Verify
- [ ] You can sign in, and you've recorded the recovery key location.
