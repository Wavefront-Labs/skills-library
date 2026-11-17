---
id: computing-software.it-support-helpdesk.intune-mdm.windows-compliance-policy-settings
name: windows-compliance-policy-settings
category: computing-software
field: it-support-helpdesk
product: intune-mdm
tags: [it-support-helpdesk, intune-mdm, windows-compliance-settings, device-health-attestation, bitlocker, secure-boot, minimum-os-version, compliance-policy]
level: practitioner
status: docs-checked
description: "Choose and support Windows compliance settings in Intune: DHA BitLocker/Secure Boot/code integrity, OS version ranges, firewall/AV/Defender checks, and why each goes noncompliant."
sources:
  - "https://learn.microsoft.com/en-us/intune/device-security/compliance/ref-windows-settings"
  - "https://learn.microsoft.com/en-us/windows/client-management/mdm/healthattestation-csp"
  - "https://learn.microsoft.com/en-us/intune/device-security/compliance/monitor-policy"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# windows-compliance-policy-settings

Each setting in a Windows compliance policy is a reason a user can be blocked by
conditional access. Choose fewer, meaningful settings and know how each is evaluated.

## Settings and how they're evaluated
| Setting | Source of truth | Common noncompliance cause |
|---|---|---|
| Require BitLocker (Device Health) | Health attestation, measured only at boot | Encryption finished but device not rebooted |
| Require Secure Boot | Health attestation | Supported on some TPM 1.2 and 2.0 devices; unsupported hardware shows Not Compliant |
| Require code integrity | Health attestation | Unsigned driver or changed system file loaded |
| Minimum / Maximum OS version | Device report, `major.minor.build.revision` (get it with `ver`) | Device behind on updates, or above the maximum (blocked) |
| Valid operating system builds | Device report; ranges with description, min and max | Missing a range for a newly deployed release |
| Encryption of data storage | DeviceStatus CSP (EncryptionCompliance); checks BitLocker at OS drive level | Unencrypted OS drive; a reboot may be needed |
| Firewall | Firewall CSP | A GPO that turns the firewall off or allows all inbound overrides Intune and gives Not compliant |
| TPM | DeviceStatus CSP | Compliant if TPM version is greater than 0 |
| Antivirus / Antispyware | Windows Security Center registered products | Product disabled or out of date |
| Defender Antimalware, minimum version, security intelligence up to date, real-time protection | Defender CSP | Service off or signatures out of date |
| Machine risk score (Clear, Low, Medium, High) | Defender for Endpoint | Threats above the chosen level |

## Choosing
- BitLocker via "Require BitLocker" (attestation) or "Encryption of data storage"; the docs
  say Require BitLocker validates at the TPM level, and either may need a reboot before the
  device shows compliant.
- OS version: **Valid operating system builds** (more flexible than min/max) lets you
  enforce patch levels across several Windows releases.
- The machine risk score needs Microsoft Defender for Endpoint integration.

## Troubleshooting a noncompliant device
1. Intune > Devices > Compliance > the policy > per-setting status report.
2. BitLocker attestation shows noncompliant after encryption: reboot, then sync.
3. Firewall showing Error right after a reboot or wake: sync manually to re-evaluate.
4. Force evaluation: Settings > Accounts > Access work or school > Info > Sync.

## Gotchas
- Compliance evaluates on check-in (about every 8 h), so fixes don't unblock instantly.
- Group policy that conflicts with a compliance setting (for example firewall) wins; remove
  it or migrate it to Intune.

## Verify
Per-setting report shows all Compliant on a test device; deliberately turning off the
firewall flips the device to Not compliant at next check-in, and back after re-enabling.

## Checked
2026-11-01. Confirmed against the Intune Learn Windows compliance settings reference:
attestation settings and boot-time measurement, OS version format and valid builds, encryption
and TPM checks, firewall GPO override, antivirus and Defender settings, risk score.
Removed: local PowerShell checks, the 2-month patch advice, the removable-drive and VM claims,
CA token cache timing, and the not-applicable state.
Method: documentation only; no commands were run.
