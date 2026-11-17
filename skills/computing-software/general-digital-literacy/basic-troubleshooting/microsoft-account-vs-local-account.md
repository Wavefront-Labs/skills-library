---
id: computing-software.general-digital-literacy.basic-troubleshooting.microsoft-account-vs-local-account
name: microsoft-account-vs-local-account
category: computing-software
field: general-digital-literacy
product: basic-troubleshooting
tags: [basic-troubleshooting, ts-accounts-signin, local-account, microsoft-account, windows-sign-in]
level: intro
status: docs-checked
description: "Understand what a Microsoft account does on Windows compared with a local account, switch between them, and keep BitLocker keys and OneDrive working."
sources:
  - https://support.microsoft.com/en-us/windows/find-your-bitlocker-recovery-key-6b71ad27-0b89-ea08-f143-056f5ab347d6
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Microsoft account vs local account

A Microsoft account signs you in with an email address and syncs settings and services; a local account exists only on
that PC. Switching either way can affect device encryption, so protect the recovery key first.

## Which do I have?
Windows Settings, Accounts, Your info shows an email address for a Microsoft account; a local account shows no email.
Menu names change between Windows versions: if a path below is not found, search Settings for "account".
Work or school PCs use "Access work or school": do not change those without your IT team.

## Before switching: BitLocker or device encryption
- Microsoft Support states it cannot retrieve, provide or recreate a lost BitLocker recovery key. Find and back up your
  recovery key (Microsoft's "Find your BitLocker recovery key" page lists where it may be stored) before you change accounts
  or hardware, or you risk losing access to the drive's data.
- Note which files live only in OneDrive (for example Desktop or Documents folders backed up to OneDrive), and back
  them up before you sign out of the account.

## Switch
In Settings, Accounts, Your info, choose the option to sign in with a Microsoft account or with a local account instead,
and follow the prompts. Check afterwards that you can sign in and that OneDrive and your apps still work.

## Gotchas
- The Windows Hello PIN belongs to that device; the account password works on any device.
- Family Safety features depend on Microsoft accounts: check Microsoft's family-safety help before removing one.

## Verify
- [ ] Your info shows the intended account type; you can sign in, and the recovery key is stored somewhere other than the PC.

## Checked
2026-10-28. Confirmed (Microsoft Support, Find your BitLocker recovery key): Microsoft cannot retrieve or recreate a lost
recovery key; recovery key backup guidance. Removed (unconfirmed; the "change from a local account to a Microsoft account"
page returned 404): comparison table claims (reset via security questions, auto-saved key location, sync behaviour), exact
button wording for switching, Windows 11 setup requirement, Control Panel backup path, Family Safety statement turned
into a pointer.
Method: documentation only; no commands were run.
