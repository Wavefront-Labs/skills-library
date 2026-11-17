---
id: computing-software.it-support-helpdesk.apple-device-management.filevault-key-escrow
name: filevault-key-escrow
category: computing-software
field: it-support-helpdesk
product: apple-device-management
tags: [it-support-helpdesk, apple-device-management, filevault, filevault-key-escrow, recovery-key, escrow]
level: practitioner
status: docs-checked
description: "Turn on FileVault by MDM with deferred enablement, escrow the personal recovery key with the FDERecoveryKeyEscrow payload and rotate it with RotateFileVaultKey."
sources:
  - "https://support.apple.com/guide/deployment/dep0a2cb7686/web"
  - "https://support.apple.com/guide/deployment/dep32bf53500/web"
  - "https://raw.githubusercontent.com/apple/device-management/release/mdm/commands/rotate.file.vault.key.yaml"
  - "https://raw.githubusercontent.com/apple/device-management/release/mdm/commands/information.security.yaml"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# filevault-key-escrow

Goal: encrypted Macs whose personal recovery key is escrowed and rotatable.

Payloads (macOS device and user channels; Device Enrolment and Automated Device Enrolment; only one of each can be delivered):
- `com.apple.MCX.FileVault2` (requires user approval): `Enable` is the only required setting. Others include `Defer` (turns on at next logout), "Use recovery key" (create and show a personal recovery key), a setting to hide the recovery key from the user, login bypass attempts (0 forces FileVault on at the next login attempt, -1 disables the limit), "Don't ask at user logout", `Output path`, `Payload certificate UUID`, and "Turn on in Set-Up Assistant" (`ForceEnableInSetupAssistant`, needs `await_device_configured`; before macOS 14.4 the interactively created account had to be an Administrator).
- `com.apple.security.FDERecoveryKeyEscrow`: `Location` (required; text shown to the user when turning on FileVault), `Encrypt certificate payload UUID` (required; a `com.apple.security.pkcs1` payload in the same profile) and optional `Device key` (replaces `RecordNumber`; the serial number is used if absent).
- `com.apple.MCX` can allow or prevent turning FileVault on or off and destroy the key on standby.

How it works
- MDM-managed FileVault is "deferred enablement": it needs a logout or login by the user. A user needs a secure token, and on Apple silicon must be a volume owner, to unlock the volume.
- The Mac encrypts the personal recovery key (PRK) asymmetrically in a CMS envelope with the escrow certificate; it returns in the security information query (`SecurityInfo`, key `FDE_PersonalRecoveryKeyCMS`; `FDE_HasPersonalRecoveryKey` and `FDE_Enabled` report state). The service itself may not be able to decrypt it.
- Rotate with the `RotateFileVaultKey` command (macOS 10.9 and later, device channel, forbidden for User Enrolment): `KeyType` `personal`, a `FileVaultUnlock` dictionary with `Password`, and optionally `ReplyEncryptionCertificate`; the response `RotateResult` holds `EncryptedNewRecoveryKey`.
- Prefer a PRK to an institutional recovery key: on Apple silicon an institutional key cannot reach recoveryOS and cannot unlock via target disk mode. There is one PRK per encrypted volume. On Apple silicon with macOS 12.0.1 or later, press Option-Shift-Return at the login screen to reveal the PRK entry field.
- `fdesetup` with a username and password to turn FileVault on is deprecated from macOS 10.15; use deferred enablement. `fdesetup remove -user` removes a user's ability to unlock.

Gotcha: because enablement is deferred until the user next logs in or out, no key is escrowed until that event; a Mac whose user never logs out or in is not covered.

Verify:
- The `SecurityInfo` response shows `FDE_Enabled` and `FDE_HasPersonalRecoveryKey` true, and a `FDE_PersonalRecoveryKeyCMS` value.
- Decrypt the escrowed PRK with your private key and confirm it unlocks a test Mac.

## Checked

Date: 2026-11-07. Read in full: Apple Platform Deployment "Manage FileVault with device management", "FileVault device management payload settings for Apple devices" and "Intro to FileVault", plus the apple/device-management `rotate.file.vault.key.yaml` and (searched, not read end to end for the FDE_* keys and bootstrap keys) `information.security.yaml`. Removed as unconfirmed: the Jamf Pro Disk Encryption steps and menu paths, `fdesetup changerecovery -personal` (replaced by the documented `RotateFileVaultKey` command), the `fdesetup status` and `list` checks, the `DeviceKey` casing, and the audit/rotate-after-use practice. Payload setting names follow the Apple page's display names where the page does not show key names.
Method: documentation only; no commands were run.
