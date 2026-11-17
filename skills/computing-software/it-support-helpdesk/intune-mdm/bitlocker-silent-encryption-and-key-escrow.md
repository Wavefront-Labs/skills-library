---
id: computing-software.it-support-helpdesk.intune-mdm.bitlocker-silent-encryption-and-key-escrow
name: bitlocker-silent-encryption-and-key-escrow
category: computing-software
field: it-support-helpdesk
product: intune-mdm
tags: [it-support-helpdesk, intune-mdm, bitlocker-silent-encryption, bitlocker, key-escrow, recovery-key-backup, endpoint-security, disk-encryption-policy, intune, bitlocker-key-rotation]
level: practitioner
status: docs-checked
description: "Enable BitLocker silently from Intune: the required settings, TPM-only startup, escrowing keys to Entra ID before encrypting, reports, and why silent encryption stalls."
sources:
  - "https://learn.microsoft.com/en-us/mem/intune/protect/encrypt-devices"
  - "https://learn.microsoft.com/en-us/windows/client-management/mdm/bitlocker-csp"
  - "https://learn.microsoft.com/en-us/troubleshoot/mem/intune/device-protection/troubleshoot-bitlocker-policies"
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# bitlocker-silent-encryption-and-key-escrow

## Policy (Endpoint security > Disk encryption > BitLocker profile)
Settings Catalog lacks the TPM startup controls needed for reliable silent enablement;
use Endpoint security or the Device configuration Endpoint protection template.
| Setting (endpoint security) | Value |
|---|---|
| Require Device Encryption | Enabled |
| Allow Warning For Other Disk Encryption | **Disabled** (suppresses the other-encryption warning) |
| Allow Standard User Encryption | Enabled (appears once the warning is Disabled; needed for standard users) |
| OS drives: Require additional authentication at startup | Enabled, then TPM startup = Allow TPM or Require TPM; startup PIN, startup key, and key and PIN = Do not allow |
| Configure Recovery Password Rotation | Consider enabling |

Device configuration template equivalents: Warning for other disk encryption = Block;
Allow standard users to enable encryption during Microsoft Entra join = Allow; user
creation of recovery key/password = Allow or Do not allow / Require; Compatible TPM
startup = Allow or Require; compatible PIN, key, and key and PIN = Do not allow.

Silent encryption cannot use a PIN or startup key. Setting any compatible TPM option to
Required or allowing a PIN/key makes silent encryption fail. Security baselines
(for example Microsoft Defender baseline) can enable PIN and key by default; review them.

Warning: Disabled warning means BitLocker proceeds even with third-party encryption
present, risking data loss; inventory first and pilot.

## Device prerequisites (silent)
- Windows 10 1803+ (admin users) or 1809+ (standard users), or Windows 11.
- Entra joined or hybrid joined; TPM 1.2 or later; native UEFI mode; Secure Boot
  enabled; WinRE configured and available.
- Encryption type is automatic: full disk on non-modern-standby devices, used space only
  on modern standby (`powercfg /a` shows S0 Low Power Idle). To force a type use the
  Settings Catalog setting "Enforce drive encryption type on operating system drives".
- Troubleshooting article nuance: TPM 2.0 needs UEFI; TPM 1.2 does not.

## Where keys go
- Silent enablement backs the recovery key up to Entra ID automatically. Entra supports
  a maximum of 200 recovery keys per device; at the limit silent encryption fails.
- View: Intune admin center > Devices > All devices > device > Monitor > Recovery keys >
  Show Recovery Key (audited as KeyManagement). Needs
  `microsoft.directory/bitlockerKeys/key/read` (Cloud Device Administrator, Helpdesk
  Administrator, Global Administrator).
- Deleting the Intune object of an Entra-joined BitLocker device removes the OS volume
  key protectors, leaving BitLocker suspended.
- Rotation: device action BitLocker key rotation (Windows 10 1909+ or Windows 11);
  needs Client-driven recovery password rotation enabled, Save BitLocker recovery
  information to Entra ID = Enabled, Store recovery information in Entra ID before
  enabling BitLocker = Required. The admin needs the Remote tasks > Rotate BitLockerKeys
  right (built in to Help Desk Operator and Endpoint Security Administrator).
- Self-service: Company Portal, account.microsoft.com, Entra; Conditional Access can
  require a compliant device to read keys.

## Why it isn't encrypting
| Check | Where |
|---|---|
| Intune encryption report | Devices > Monitor > Encryption report |
| Was policy applied | Event log Microsoft-Windows-DeviceManagement-Enterprise-Diagnostics-Provider > Admin; search `BitLocker`, entries look like `./Device/Vendor/MSFT/BitLocker/RequireDeviceEncryption` |
| Encryption errors | Event Viewer > Applications and Services Logs > Microsoft > Windows > BitLocker-API (Management) |
| "Failed to enable Silent Encryption ... conflicting Group Policy settings" | Set compatible TPM startup PIN (and key) to Blocked |
| "TPM is not available" | `tpm.msc` or `get-tpm` |
| WinRE errors | `reagentc /info`, then `reagentc /enable` as admin |
| Nothing in BitLocker-API | Run the task "BitLocker MDM policy Refresh" in Task Scheduler > Microsoft > Windows > BitLocker; enable the TaskScheduler Operational log first |
| Method mismatch (e.g. policy XTS-AES 256, device XTS-AES 128) | `manage-bde -status` shows method; mismatch causes reporting errors |
| Settings applied on client | `HKLM\SOFTWARE\Microsoft\PolicyManager\current\device\BitLocker` and `HKLM\SOFTWARE\Policies\Microsoft\FVE`; MDM diagnostic report at `Users\Public\Documents\MDMDiagnostics` on the system drive |

Do a manual sync first: Settings > Accounts > Access work or school > account > Info > Sync.

## Gotchas
- CSP: AllowStandardUserEncryption works only when AllowWarningForOtherDiskEncryption
  is 0 and RequireDeviceEncryption is 1.
- CSP setting availability by version: AllowStandardUserEncryption 1809,
  ConfigureRecoveryPasswordRotation and RotateRecoveryPasswords 1909.
- Configuring overlapping policies (Endpoint security and Endpoint protection template)
  can conflict; use Intune policy conflict detection.

## Verify
`manage-bde -status C:` shows the Conversion Status (Used Space Only Encrypted or Fully
Encrypted) and protectors; the Intune encryption report shows success and the Recovery
keys page shows a key for the device.

## Checked
Date: 2026-11-07. Read in full: the Intune BitLocker encryption article and the
client-side BitLocker troubleshooting article. Searched (not read end to end) the
BitLocker CSP for AllowStandardUserEncryption, AllowWarningForOtherDiskEncryption and
RequireDeviceEncryption behaviour.
Removed as unconfirmed: the PowerShell `BackupToAAD-BitLockerKeyProtector` / `Get-BitLockerVolume` escrow
snippet, hybrid AD escrow via GPO, "Secure Boot recommended" (silent needs it per
Intune article, though the troubleshooting page says not required), "consumer OOBE device encryption"
note, "decrypt and re-encrypt" advice, and the hardware test row. Corrected: TPM 2.0 needs UEFI;
"XTS-AES 128 or 256" and the "Do not enable until stored" wording replaced with exact
rotation prerequisites.
Method: documentation only; no commands were run.
