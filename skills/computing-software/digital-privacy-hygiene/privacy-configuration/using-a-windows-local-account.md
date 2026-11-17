---
id: computing-software.digital-privacy-hygiene.privacy-configuration.using-a-windows-local-account
name: using-a-windows-local-account
category: computing-software
field: digital-privacy-hygiene
product: privacy-configuration
tags: [digital-privacy-hygiene, privacy-configuration, windows-local-account, microsoft-account, windows, oobe, bitlocker, rufus]
level: practitioner
status: draft
description: "Set up or switch Windows to a local account instead of a Microsoft account, weighing the trade-offs (BitLocker key escrow, sync) and handling the setup-time restrictions."
sources:
  - "https://support.microsoft.com/windows"
  - "https://rufus.ie/"
  - "https://learn.microsoft.com/en-us/windows-hardware/customize/desktop/unattend/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Using a Windows local account

**Goal:** sign in to Windows without tying the PC's activity to a Microsoft account, while keeping
encryption and recovery working.

## Trade-offs first
| Microsoft account | Local account |
|---|---|
| BitLocker/Device Encryption recovery key auto-saved to the account | You must save the key yourself |
| Home edition **Device encryption** turns on automatically after MSA sign-in | Home may stay unencrypted |
| Settings/Edge sync, Store, OneDrive, Find my device | None unless you sign in per app |
| Password reset online | Reset only via security questions/another admin |

## Switch an existing PC
Settings > Accounts > Your info > **Sign in with a local account instead** (wording varies; Microsoft has been
hiding it). Alternative: create a new local admin (`net user <name> * /add` then `net localgroup Administrators
<name> /add`), sign into it, and remove the Microsoft account from Settings > Accounts > Other users.

## New installs
Windows 11 setup increasingly forces an online account, and Microsoft keeps removing the bypasses
(`OOBE\BYPASSNRO`, `start ms-cxh:localonly`). Durable options:
- Create install media with **Rufus** and tick "Remove requirement for an online Microsoft account".
- Use an `autounattend.xml` answer file that defines a local account.
- Or complete setup with a Microsoft account and switch afterwards.

## After switching
1. Check encryption: `manage-bde -status C:`. On Pro, turn on BitLocker; on Home without Device encryption,
   consider VeraCrypt system encryption or Pro upgrade.
2. **Back up the recovery key** (`manage-bde -protectors -get C:`) to your password manager and paper.
3. Remove the old key from account.microsoft.com/devices/recoverykey only after the new one is saved.
4. Sign in to Store/Office apps individually ("this app only") rather than adding the account to Windows.

## Verify
- [ ] Settings > Accounts shows "Local account"; BitLocker on with recovery key stored outside the PC.
