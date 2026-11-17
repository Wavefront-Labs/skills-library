---
id: computing-software.digital-forensics-incident-response.evidence-handling.acquiring-bitlocker-and-encrypted-volumes
name: acquiring-bitlocker-and-encrypted-volumes
category: computing-software
field: digital-forensics-incident-response
product: evidence-handling
tags: [bitlocker, encrypted-volume, full-disk-encryption, dislocker, recovery-key, forensic-acquisition, dfir]
level: advanced
status: docs-checked
description: "Access BitLocker evidence: recovery password, key, key package and DRA options, where AD DS and Entra ID store them, and libbde and dislocker."
sources: ["https://learn.microsoft.com/en-us/windows/security/operating-system-security/data-protection/bitlocker/recovery-overview", "https://github.com/Aorimn/dislocker", "https://github.com/libyal/libbde"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Acquiring BitLocker volumes

**Goal:** end up with readable plaintext of a BitLocker volume by capturing it while unlocked or by obtaining keys legitimately. Always keep a copy of the encrypted original.

## Recovery options Microsoft documents
- **Recovery password:** a 48-digit number that unlocks a volume in recovery mode. It may be saved as a text file, printed, or stored in Microsoft Entra ID or Active Directory. It is unique to the device it was created on, and holding it unlocks the volume and all its data, so control access and keep it separate from the devices.
- **Recovery key:** a key on removable media; the file name format is `<protector_id>.bek`.
- **Key package:** a decryption key for the BitLocker Repair tool to reconstruct parts of a corrupted drive; used with the recovery password or key, and only valid for the drive with the matching identifier. It is not generated automatically, can be saved to a file or AD DS, and cannot be stored in Entra ID. `manage-bde.exe -KeyPackage C: -id <id> -path <path>` creates one, needing local administrator access to the unlocked volume.
- **Data Recovery Agent (DRA) certificate:** unlocks any drive configured with the matching public key. For an OS drive, mount it as a data drive on another device.

## Where corporate recovery data lives
- **Microsoft Entra ID** (Entra joined devices): stored as a `bitlockerRecoveryKey` resource, retrievable from the Microsoft Entra admin center, the Microsoft Intune admin center (for Intune-enrolled devices), PowerShell or Microsoft Graph.
- **AD DS** (domain joined): stored as a child object of the computer object, named from the creation date and time plus the recovery GUID (63 characters). The object's common name is `ms-FVE-RecoveryInformation`, with attributes `ms-FVE-RecoveryPassword`, `ms-FVE-RecoveryGuid` (the GUID shown on the recovery screen, used to pick the right password), `ms-FVE-VolumeGuid` and `ms-FVE-KeyPackage`. More than one object can exist per computer, and AD keeps old ones unless the computer object is deleted.
- Devices that are not domain members may store the key in the user's Microsoft account. Record the key ID you matched to the volume.

## Offline readers on Linux
- **dislocker** reads BitLocker partitions, including BitLocker To Go. `dislocker-fuse` presents a `dislocker-file` virtual NTFS partition (writes to it change the underlying partition, so do not write); `dislocker-file` decrypts to a flat NTFS file of the same size as the volume, with no link back to the original. See dislocker(1) for options.
- **libbde** (status: alpha) reads Vista, Windows 7 and later, To Go and used-disk-space-only formats, with AES-CBC (with or without Elephant diffuser) and AES-XTS. Supported protectors: clear key, password, recovery password, start-up key, FVEK/TWEAK key data. TPM and SID-based protectors are unsupported, so a TPM-only volume needs another route (recovery password or key). Project docs are on its wiki.
- Work on an image or a read-only device, mount the decrypted output read-only.

## Gotchas
- Keys and passphrases are sensitive; record their source in notes, not in reports.
- Hash the encrypted image before and after your work.

## Checked
Confirmed against the Microsoft BitLocker recovery overview (recovery password, key, key package, DRA, Entra ID and AD DS storage, ms-FVE attributes, KeyPackage command), the dislocker README (dislocker-fuse, dislocker-file, To Go support) and the libbde README (formats, encryption and protection methods, alpha status). Removed unconfirmed content: FileVault, LUKS and VeraCrypt coverage, manage-bde -status and Get-BitLockerVolume output, AD PowerShell and Graph path, memory and hiberfil key extraction, libbde and dislocker command lines, FTK Imager and Arsenal Image Mounter steps.

Method: docs-only read of cited pages, 2026-11-09
