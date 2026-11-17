---
id: computing-software.cybersecurity-defensive.endpoint-security.microsoft-defender-antivirus-configuration
name: microsoft-defender-antivirus-configuration
category: computing-software
field: cybersecurity-defensive
product: endpoint-security
tags: [antimalware, microsoft-defender-antivirus, mpcmdrun, set-mppreference, scheduled-scans, pua-protection, network-protection, passive-mode]
level: practitioner
status: docs-checked
description: "Configure Microsoft Defender Antivirus centrally: real-time and cloud settings, PUA, network protection, scan schedules, exclusions discipline and passive vs active mode."
sources: ["https://learn.microsoft.com/en-us/powershell/module/defender/set-mppreference", "https://learn.microsoft.com/en-us/defender-endpoint/microsoft-defender-antivirus-compatibility", "https://learn.microsoft.com/en-us/powershell/module/defender/start-mpscan"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Microsoft Defender Antivirus configuration

**Goal:** a consistently configured, tamper-protected antivirus layer on every Windows device,
managed centrally and verified.

## Key settings (Intune Endpoint security > Antivirus, GPO, or PowerShell)
```powershell
Set-MpPreference -DisableRealtimeMonitoring $false
Set-MpPreference -MAPSReporting Advanced -SubmitSamplesConsent SendSafeSamples
Set-MpPreference -CloudBlockLevel High -CloudExtendedTimeout 50
Set-MpPreference -PUAProtection Enabled
Set-MpPreference -EnableNetworkProtection Enabled
Set-MpPreference -ScanParameters QuickScan -ScanScheduleDay Everyday -ScanScheduleQuickScanTime 12:00:00
Set-MpPreference -SignatureUpdateInterval 4
Set-MpPreference -DisableArchiveScanning $false -DisableEmailScanning $false
```
Manage via Intune/GPO in production; local `Set-MpPreference` is for testing (tamper protection blocks many local changes).

## Modes
- **Active**: Defender is the primary AV.
- **Passive**: another AV is primary; Defender scans on demand and feeds Defender for Endpoint (with EDR in block mode for post-breach blocking).
- Check: `Get-MpComputerStatus | Select AMRunningMode, RealTimeProtectionEnabled, IsTamperProtected, AntivirusSignatureLastUpdated`.

## Exclusions discipline
- Exclusions are a common attacker hiding place and a frequent misconfiguration. Exclude only per vendor guidance (e.g. specific database files), by full path and process, never whole drives or `%TEMP%`.
- Review exclusions quarterly; local admins should not be able to add them (see the policy-merge settings in the Defender Antivirus exclusion documentation).

## Operations
- Update signatures through your management channel and monitor signature age.
- On-demand scan: `Start-MpScan -ScanType FullScan`.
- Threat history: `Get-MpThreatDetection`.
- Reporting: Defender portal device health / Intune antivirus reports for outdated signatures and disabled protection.

## Gotchas
- Two real-time AV products in active mode cause performance problems; ensure only one is active.
- Servers: Defender on Windows Server includes automatic role-based exclusions; do not duplicate them manually.
- Signature updates failing behind proxies are common; monitor signature age.

## Checked
2026-10-28. Confirmed in the Set-MpPreference, Start-MpScan, Get-MpThreatDetection and antivirus compatibility pages: every `Set-MpPreference` parameter used (`-MAPSReporting`, `-SubmitSamplesConsent`, `-CloudBlockLevel`, `-CloudExtendedTimeout`, `-PUAProtection`, `-EnableNetworkProtection`, `-ScanParameters`, `-ScanScheduleDay`, `-ScanScheduleQuickScanTime`, `-SignatureUpdateInterval`). Removed: `DisableLocalAdminMerge`, the `MpCmdRun.exe` command lines and the 99% figure.
Method: documentation only; no commands were run.

## Verify
- [ ] EICAR test file is detected and quarantined.
- [ ] Fleet report: real-time on, tamper protection on, signatures current on all devices.
