---
id: computing-software.systems-network-administration.windows-server.bitlocker-on-server-volumes
name: bitlocker-on-server-volumes
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, bitlocker, enable-bitlocker, manage-bde, tpm, recovery-password, bitlocker-feature, used-space-only, xts-aes, bitlocker-auto-unlock]
level: practitioner
status: docs-checked
description: "Enable BitLocker on Windows Server OS and data volumes: install the feature, TPM protector, recovery password, auto-unlock for data volumes and status checks."
sources:
  - https://learn.microsoft.com/en-us/windows/security/operating-system-security/data-protection/bitlocker/operations-guide
  - https://learn.microsoft.com/en-us/powershell/module/bitlocker/enable-bitlocker
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# BitLocker on server OS and data volumes

## Install
```powershell
Get-Tpm | Select TpmPresent,TpmReady
```

## OS volume
```powershell
Enable-BitLocker -MountPoint $env:SystemDrive -EncryptionMethod XtsAes256 -UsedSpaceOnly -TpmProtector
Add-BitLockerKeyProtector -MountPoint $env:SystemDrive -RecoveryPasswordProtector
```
- Add the recovery password **before** relying on it; store it (AD DS, Entra, vault).
- `-UsedSpaceOnly` is fine for new volumes; full encryption for disks that held data.

## Data volumes
```powershell
Enable-BitLocker -MountPoint 'E:' -EncryptionMethod XtsAes256 -RecoveryPasswordProtector
Enable-BitLockerAutoUnlock -MountPoint 'E:'
```

## manage-bde
```
manage-bde -protectors -disable C: -RebootCount 1     # firmware update
```

## Gotchas
- Suspend protection for BIOS/firmware updates (`Suspend-BitLocker -RebootCount 1`), or
  the next boot asks for the recovery key.

## Verify
- [ ] `Get-BitLockerVolume` shows the volume encrypted with the expected key protectors.
- [ ] Recovery password escrowed and retrievable.

## Checked
2026-10-28: Confirmed on Learn pages enable-bitlocker, enable-bitlockerautounlock, suspend-bitlocker, manage-bde-protectors and get-tpm: Enable-BitLocker -EncryptionMethod XtsAes256 -UsedSpaceOnly -TpmProtector, Add-BitLockerKeyProtector -RecoveryPasswordProtector, Suspend-BitLocker -RebootCount, manage-bde -protectors -disable -RebootCount, Get-BitLockerVolume, Get-Tpm. Removed: feature install, VM TPM and Azure encryption notes, manage-bde -on/-unlock/-status, TPM+PIN/Network Unlock claims, auto-unlock precondition, Server Core note.
Method: documentation only; no commands were run.
