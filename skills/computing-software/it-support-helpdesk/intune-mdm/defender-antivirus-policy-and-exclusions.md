---
id: computing-software.it-support-helpdesk.intune-mdm.defender-antivirus-policy-and-exclusions
name: defender-antivirus-policy-and-exclusions
category: computing-software
field: it-support-helpdesk
product: intune-mdm
tags: [it-support-helpdesk, intune-mdm, defender-antivirus-policy, microsoft-defender, antivirus-exclusions, tamper-protection, endpoint-security, mpcmdrun, intune, defender-remote-scan]
level: practitioner
status: docs-checked
description: "Manage Defender Antivirus from Intune endpoint security: profiles, exclusions and policy merge, tamper protection, controlled configuration, checking exclusions."
sources:
  - "https://learn.microsoft.com/en-us/mem/intune/protect/endpoint-security-antivirus-policy"
  - "https://learn.microsoft.com/en-us/defender-endpoint/configure-exclusions-microsoft-defender-antivirus"
  - "https://learn.microsoft.com/en-us/defender-endpoint/prevent-changes-to-security-settings-with-tamper-protection"
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# defender-antivirus-policy-and-exclusions

## Where the policy lives
Intune admin center > Endpoint security > Antivirus (Manage). Windows profiles (platform "Windows", which replaced "Windows 10 and later" on 5 April 2022): Microsoft Defender Antivirus, Microsoft Defender Antivirus exclusions, Windows Security experience, Defender Update controls (engine, platform and security intelligence update channels). macOS has an Antivirus profile that replaces .plist configuration but needs Defender for Endpoint installed. Linux has Microsoft Defender Antivirus and exclusions profiles. Windows Server is supported through the Defender for Endpoint security settings management scenario. The Antivirus profile is separate from the antivirus settings in a Device Restrictions profile, and unlike those it works on co-managed devices when the Endpoint Protection workload slider is set to Intune. The per-setting recommended values are not given on the cited pages: take them from your security baseline.

## Tamper protection and controlled configuration
- Manage it in the **Windows Security experience** profile (Antivirus policy). Devices must be onboarded to Defender for Endpoint (P1 or P2); until then it shows Not applicable, and it takes effect at the first check-in after onboarding.
- When on (Windows), these cannot be changed: real-time protection, behaviour monitoring, IOAV, cloud protection, security intelligence updates, automatic actions on threats, Windows Security notifications, scanning of archives, exclusions (see "Protect Microsoft Defender Antivirus exclusions with tamper protection"); registry changes to Defender settings are blocked. Changes made by a management tool or Group Policy can appear to succeed but be blocked; use troubleshooting mode to change a protected setting temporarily.
- Controlled configuration (preview) goes further: the Controlled Configuration (Device) setting in the Windows Security experience profile has values Not configured, Off (default, turns off both), Tamper Protection (On) and Controlled Configuration (On). Intune-delivered Antivirus and ASR settings then override Group Policy, Configuration Manager and local changes; settings not configured fall back to secure defaults. It does not apply to EDR, firewall, or Settings Catalog policies (overlapping settings there report Not applicable).
- Intune can manage tamper protection on macOS, Windows 10 and 11 (including Enterprise multi-session), Windows Server 2016 and later, Windows Server 1803 or later, and Windows Server 2012 R2 (modern unified solution).
- Managing via Intune also requires an Intune license, devices not co-managed, and DisableLocalAdminMerge set to true.

## Exclusions done right
Use a **Microsoft Defender Antivirus exclusions** profile (or the same settings in the Microsoft Defender Antivirus profile; Intune merges exclusions from all assigned policies into one superset, since ExcludedPaths, ExcludedExtensions and ExcludedProcesses support policy merge). Defining exclusions lowers protection: only exclude what you know is not malicious.
1. **Excluded processes**: files opened by the named process are not scanned; the process itself is not excluded (add an Excluded paths entry for that). Process exclusions apply only to real-time protection, not scheduled or on-demand scans.
2. **Excluded paths** (file and folder, wildcards and system, not user, environment variables supported, plus contextual exclusions such as a scan trigger).
3. **Excluded extensions**: apply to any file with that extension anywhere; use sparingly.
Document each exclusion with ticket, vendor guidance and review date. Intune settings overwrite conflicting Group Policy or PowerShell exclusions on startup, so pick one management source. The cited pages do not list which paths to avoid; read Microsoft's "Exclusions to avoid" article before adding broad ones.

Other methods listed on the page: Defender portal endpoint security policies, Policy CSP (`./Device/Vendor/MSFT/Policy/Config/Defender/ExcludedPaths`, `ExcludedExtensions`, `ExcludedProcesses`, values separated by `|`), Configuration Manager, Group Policy, PowerShell, WMI, Windows Security app (per device, no contextual exclusions).

## Check what's effective on a device
```powershell
Get-MpPreference | Select ExclusionPath, ExclusionProcess, ExclusionExtension
```
With HideExclusionsFromLocalAdmins on, exclusions are not visible in `Get-MpPreference` or the registry editor (they are not removed). To test a path (Defender platform version 4.18.2111-5.0 or later), run from an elevated prompt in the newest folder under `%ProgramData%\Microsoft\Windows Defender\Platform\` (or `%ProgramFiles%\Windows Defender`):
```
MpCmdRun.exe -CheckExclusion -Path <PathAndFile or Path>
```
Exit code 0 means excluded, 1 not excluded; a folder exclusion also covers its subfolders, and the output does not say which entry matched.

## Validate with EICAR
Defender always detects the EICAR test string by content. Create an EICAR file whose name, extension or folder matches the exclusion: not detected means the exclusion works. This does not validate process exclusions. Use a spare test device.

## Reports
Endpoint security > Antivirus has Summary and Unhealthy endpoints (MDM-managed Windows devices with detected issues only); Reports has Antivirus agent status and Detected malware.

## Verify
The per-setting report shows Succeeded, `-CheckExclusion` returns the expected result, and Windows Security shows the intended tamper protection state.

## Checked
Method: documentation only; no commands were run. Checked 2026-11-08 against the Intune antivirus policy page, the Defender exclusions configuration page and the tamper protection overview (all read in full). Removed because the cited pages do not support them: the baseline settings table (cloud block level, timeouts, scan schedules), Get-MpComputerStatus and MpCmdRun -SignatureUpdate/-GetFiles/-Restore usage, the false-positive workflow, the "never exclude" list, and the Passive mode and GPO merge gotchas.
