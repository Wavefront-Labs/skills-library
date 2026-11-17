---
id: computing-software.systems-network-administration.windows-server.bitlocker-group-policy-settings
name: bitlocker-group-policy-settings
category: computing-software
field: systems-network-administration
product: windows-server
tags: [bitlocker, bitlocker-gpo, xts-aes, group-policy, tpm]
level: practitioner
status: docs-checked
description: "Configure BitLocker by Group Policy: encryption method and cipher strength, startup authentication, recovery options with AD DS backup, and hardware encryption."
sources:
  - https://learn.microsoft.com/en-us/windows/security/operating-system-security/data-protection/bitlocker/configure
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# BitLocker Group Policy settings

Path: Computer Configuration > Administrative Templates > Windows Components > BitLocker Drive Encryption.

## Encryption method
**Choose drive encryption method and cipher strength**: Microsoft recommends the XTS-AES algorithm for
all drives. Choose a 256-bit key on more performant disks and CPUs and 128-bit on less performant ones.
If the policy is disabled or not configured, BitLocker uses XTS-AES 128-bit. The policy is ignored
for self-encrypting fixed and OS drives. Set it before encryption starts: it governs the method
used when a volume is encrypted.

## Operating System Drives
- **Require additional authentication at startup**: sets the TPM, PIN and startup-key combinations.
  Choose by physical exposure of the server (unattended reboot vs a PIN typed at the console).
- **Choose how BitLocker-protected operating system drives can be recovered**: under *Save BitLocker
  recovery information to Active Directory Domain Services* choose *Backup recovery password and key
  package* (the key package supports recovery from a physically corrupted drive) or *Backup recovery
  password only*. *Do not enable BitLocker until recovery information is stored in AD DS for operating
  system drives* blocks enabling BitLocker unless the device is connected to the domain and the backup
  succeeds; a recovery password is then generated automatically.
- **Enforce drive encryption type on operating system drives**: sets full or used-space-only encryption
  for non-silent encryption (silent encryption supports full encryption only).
- **Configure use of hardware-based encryption for operating system drives**: if disabled, BitLocker
  cannot use hardware encryption and uses software encryption; if not configured, software encryption
  is used regardless of hardware support.

## Fixed Data Drives
The same families exist for fixed drives: enable *Do not enable BitLocker until recovery information is
stored in AD DS for fixed data drives* for the same escrow guarantee, plus the matching enforce-type and
hardware-encryption policies.

## Network Unlock
The policy lets TPM-equipped devices with a Network Unlock certificate create Network Key Protectors;
the certificate is distributed via *Public Key Policies > BitLocker Drive Encryption Network Unlock Certificate*.

## Verify
- [ ] The policy is applied on the server (run `gpresult`), every volume uses the intended method, and a
  recovery object exists in AD DS for each protected volume.

## Checked
2026-10-28. Confirmed against the Learn page "BitLocker group policy settings" (policy names, XTS-AES recommendation and the XTS-AES 128 default, AD DS backup options and blocking setting, hardware-based encryption behaviour, enforce-type note, Network Unlock). Removed as unconfirmed: the claim to use 256-bit for all fixed drives, AES-CBC for removable drives, server-specific TPM guidance, auto-unlock default, `Enable-BitLocker` and `Get-ADObject` commands and the "disable hardware encryption because of firmware bugs" advice.
Method: documentation only; no commands were run.
