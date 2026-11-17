---
id: computing-software.digital-privacy-hygiene.two-factor-auth.microsoft-authenticator-backup-and-restore
name: microsoft-authenticator-backup-and-restore
category: computing-software
field: digital-privacy-hygiene
product: two-factor-auth
tags: [digital-privacy-hygiene, two-factor-auth, microsoft-authenticator-backup, authenticator-migration, microsoft-account-2fa]
level: practitioner
status: docs-checked
description: "Turn on Microsoft Authenticator backup, restore to a new phone of the same type, and know which work, school and passkey accounts must be re-registered."
sources:
  - "https://support.microsoft.com/account-billing/back-up-and-recover-account-credentials-in-the-authenticator-app-bb939936-7a8d-4e88-bc43-49bc1a700a40"
  - "https://learn.microsoft.com/entra/identity/authentication/concept-authentication-authenticator-app"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Microsoft Authenticator backup and restore

**Goal:** a new phone gets your codes back, and you know in advance which accounts won't come along.

## What is backed up
- One-time password codes (30-second codes) for personal Microsoft accounts and
  third-party accounts such as LinkedIn and Facebook.
- Passwordless credentials of personal Microsoft accounts are **not** backed up; only the
  account name is saved and you sign in again after restoring.
- **Work or school account** credentials are not backed up; only the account name is
  saved, and you must sign in and register the account again on the new device.
- Passkeys in Authenticator for Entra ID are device-bound: they never leave the device
  they were created on, so register a new one on the new phone.

## Turn on backup
- **Android:** open Authenticator > menu > Settings > turn on the **Cloud Backup** toggle >
  select a Microsoft personal account to hold the backup > OK. To change the recovery
  account, delete the existing backup (toggle off, OK) and make a new one. The page
  notes that starting January 2027 Android backup will use Google One backup instead of
  a Microsoft personal account.
- **iOS:** enable iCloud Drive, iCloud Keychain and iCloud Backup, then find Authenticator
  in the Saved to iCloud list and turn its toggle on.

## Restore on a new phone
1. Install Authenticator and use its restore option. The new phone must be the same type:
   a backup made on iOS cannot be restored on Android, or the reverse.
2. If the backup does not appear (iOS): on the old phone have the three iCloud settings and
   the Authenticator toggle on, update to version 6.8.33 or later, and open the app at
   least once before switching; on the new phone uninstall and reinstall Authenticator.
3. "Something went wrong" when backing up means you are not signed in: under Backup, turn
   Cloud Backup on and choose Continue or Change account to sign in.

## Before you wipe the old phone
- Confirm that the backup exists and the right recovery account is used.
- For work or school accounts, plan to re-register on the new phone; ask your IT
  help desk if you cannot sign in.
- Switching between iPhone and Android means re-enrolling each account.

## Checked
Checked 2026-11-08 against the Microsoft support page "Back up one-time password codes in
Microsoft Authenticator" and the Entra Authenticator concept page (device-bound passkeys).
Removed: Settings > Backup menu names for iOS, a "Begin recovery" label, aka.ms links,
the "last backup" display and the password autofill removal claim, none of which the
pages state.

Method: docs-only read of cited pages, 2026-11-08
