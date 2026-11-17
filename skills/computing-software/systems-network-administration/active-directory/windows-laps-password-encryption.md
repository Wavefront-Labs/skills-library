---
id: computing-software.systems-network-administration.active-directory.windows-laps-password-encryption
name: windows-laps-password-encryption
category: computing-software
field: systems-network-administration
product: active-directory
tags: [windows-laps, laps-encryption, authorized-password-decryptors, dpapi-ng, active-directory]
level: advanced
status: docs-checked
description: "Enable Windows LAPS password encryption in AD: domain functional level needs, choosing authorized decryptors, history and what breaks if misconfigured."
sources:
  - https://learn.microsoft.com/en-us/windows-server/identity/laps/laps-concepts-overview
  - https://learn.microsoft.com/en-us/windows-server/identity/laps/laps-management-policy-settings
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Windows LAPS password encryption

Without encryption, Windows LAPS stores the password in clear text in `msLAPS-Password`, protected only by attribute ACLs.
With encryption, the managed device encrypts the password (CNG DPAPI, AES-256) before sending it to AD, so only one chosen
principal can decrypt it even if others can read the attribute.

## Requirements
- Domain functional level **Windows Server 2016** or later. Microsoft does not support retrieving previously decrypted LAPS
  passwords in a domain below the 2016 DFL.
- Active Directory backup (encryption is an AD feature; it does not apply to Entra backup).
- Microsoft highly recommends enabling it for AD-stored passwords.

## Policy settings
- **ADPasswordEncryptionEnabled**: 1 or 0; the page documents no default, so set it explicitly. It requires DFL 2016 or
  later. (`PasswordExpirationProtectionEnabled`, a different setting, defaults to True.)
- **ADPasswordEncryptionPrincipal** (authorized decryptors): a single user or group. If not set, the Domain Admins group of
  the managed device's domain is used. The device checks the principal resolves before encrypting. Only one principal is
  supported; to allow several, create a wrapper group. The authorized principal cannot be changed for a password that is
  already encrypted. The setting is ignored for DSRM backups (always Domain Admins of the DC's domain).
- **ADEncryptedPasswordHistorySize**: 0 to 12, default 0. History needs encryption on, and lets you recover an earlier
  password after a restore from backup.
- **ADBackupDSRMPassword**: encrypted DSRM backup for DCs (the decryptor is always Domain Admins of the DC's domain).

Encrypted values go to `msLAPS-EncryptedPassword` and `msLAPS-EncryptedPasswordHistory`; with encryption on, the clear-text
`msLAPS-Password` attribute is not used.

## Read
```powershell
Get-LapsADPassword -Identity APP01 -AsPlainText
Get-LapsADPassword -Identity APP01 -IncludeHistory -AsPlainText
```
The caller needs read permission on the password attributes (`Set-LapsADReadPasswordPermission`) **and** must be the
authorized decryptor (or a member of that group). Use `-DecryptionCredential` to supply a different account for decryption.

## Gotchas
- A password that is already encrypted keeps its authorized principal. After you change the principal, rotate the
  password (`Reset-LapsPassword` on the client, or expire it with `Set-LapsADPasswordExpirationTime`) so the new password is
  encrypted to the new principal.
- Use different decryptor groups for servers, workstations and DCs by applying different GPOs to different OUs.
- Password history is supported only when encryption is enabled, not for clear-text passwords.

## Verify
- [ ] `msLAPS-EncryptedPassword` is populated on sample computers.
- [ ] A helpdesk account that can read the attribute but is not a decryptor cannot recover the password.

## Checked
Checked 2026-10-27 against Microsoft Learn (windowsserverdocs LAPS concepts overview dated 2025-05-12, LAPS policy
settings dated 2025-06-26, technical reference and the LAPS PowerShell reference for Windows Server 2025). Confirmed the DFL,
default decryptor, single-principal limit, history range, attribute names and cmdlet parameters. Corrected: the default
decryptor is Domain Admins of the device's domain (not a configurable group), the "April 2023 builds" claim is dropped,
and a changed principal needs a password rotation to take effect. Removed the KDS root key statement, which the pages do not make.
Method: documentation only; no commands were run.
