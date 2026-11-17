---
id: computing-software.it-support-helpdesk.apple-device-management.secure-token-volume-owner
name: secure-token-volume-owner
category: computing-software
field: it-support-helpdesk
product: apple-device-management
tags: [it-support-helpdesk, apple-device-management, filevault, secure-token-volume-owner, secure-token, volume-owner]
level: practitioner
status: docs-checked
description: "Diagnose Secure Token and Volume Owner problems on Apple silicon Macs with diskutil apfs listUsers, fdesetup list -extended and the bootstrap token."
sources:
  - "https://support.apple.com/guide/deployment/dep24dbdcf9e/web"
  - "https://support.apple.com/guide/deployment/dep82064ec40/web"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# secure-token-volume-owner

Goal: know which accounts can unlock the disk and authorise changes.

- Volume owners on Apple silicon: `sudo diskutil apfs listUsers /`. GUIDs of type "Local Open Directory User" map to the `GeneratedUID` attribute of user records. Secure token and FileVault users: `sudo fdesetup list -extended`.
- The user who first claims an Apple silicon Mac is granted a secure token and is the first volume owner. A volume owner is needed to change startup security policy, authorise macOS updates and upgrades, and initiate Erase All Content and Settings.
- Volume owner and administrator are separate: changing startup security needs both; authorising software updates needs only ownership (a standard user can do it).
- A bootstrap token (macOS 10.15.4 or later) is escrowed to the MDM service at first login of a secure token user, becomes a volume owner and grants secure tokens, and so volume ownership, to later accounts when they log in (macOS 11 or later).
- Changing token status with `sysadminctl` always needs an existing secure-token administrator's credentials, interactively or via `-adminUser` and `-adminPassword`. Scripted user creation with `sysadminctl` needs the same to give the new user a token. macOS prevents deleting the last administrator or secure-token user.
- macOS 11 or later: the first user whose password is set gets a token. To stop this for a programmatically created user, add `;DisabledTags;SecureToken` to its `AuthenticationAuthority` before setting the password (Apple shows `dscl . -append`).
- Bootstrap token tooling: `sudo profiles status -type bootstraptoken` reports service support and local state; `install` generates and escrows one (needs existing secure-token admin details); `remove` deletes it.

Gotcha: a user without a secure token is not offered to unlock a FileVault volume; give tokens via the bootstrap token at login or an existing token holder's credentials.

Verify:
- `fdesetup list -extended` and `diskutil apfs listUsers /` include the account you expect.
- `profiles status -type bootstraptoken` shows the service supports it and a token is escrowed.

## Checked

Date: 2026-11-07. Read in full: Apple Platform Deployment "Use secure token, bootstrap token and volume ownership in deployments". "Intro to FileVault" was read for the FileVault context. Removed as unconfirmed: `sysadminctl -secureTokenStatus`, `-secureTokenOn` syntax, the "do not delete the original Volume Owner" rule, the "ENABLED" status string and the pre-boot unlock screen claim; the MDM-created admin gotcha was replaced with the page's bootstrap token behaviour. The old developer.apple.com source was dropped as unreadable.
Method: documentation only; no commands were run.
