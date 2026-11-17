---
id: computing-software.general-digital-literacy.basic-troubleshooting.running-a-microsoft-defender-scan
name: running-a-microsoft-defender-scan
category: computing-software
field: general-digital-literacy
product: basic-troubleshooting
tags: [basic-troubleshooting, malware, antivirus, microsoft-defender, windows-security, full-scan, offline-scan, protection-history, quarantine]
level: intro
status: docs-checked
description: "Run Microsoft Defender quick, full, custom and offline scans in Windows Security, read Protection history, and check real-time protection, cloud protection and updates."
sources:
  - https://support.microsoft.com/en-us/windows/security/threat-malware-protection/virus-and-threat-protection-in-the-windows-security-app
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Running a Microsoft Defender scan

**Goal:** check a Windows PC for malware with the built-in antivirus.

## Open Windows Security
Windows Security app > **Virus & threat protection**. (Settings > Privacy & security > Windows Security also opens it.)

## Scan types (Scan options under Current threats)
| Scan | What Microsoft says it does |
|---|---|
| Quick scan | Saves time compared with a full scan; you are notified if a different scan is recommended |
| Full scan | Scans every file and program on the device |
| Custom scan | Scans only the files and folders you select |
| Microsoft Defender Antivirus (offline scan) | Restarts the device and scans in the Windows Recovery Environment before Windows loads, so persistent malware has a harder time hiding; save open files first. Use it if you are concerned about malware or want to scan without an internet connection |

## Read the results
- After an offline scan, open Windows Security > **Protection history** to see the results.
- Under Current threats you can see quarantined threats and items you allowed. The **Allowed threats** page lists threats you chose to allow; select one and **Don't allow** so Windows Security acts on it again.
- Windows Security takes no action against threats you allow, so allow only items you are sure are safe.

## Keep it working
- **Virus & threat protection settings > Manage settings:** *Real-time protection* (can be turned off temporarily but turns itself back on after a while), *Cloud-delivered protection*, and *Tamper protection*, which must be turned off before real-time protection can be turned off.
- **Protection updates > Check for updates:** security intelligence normally arrives with Windows Update.
- If you install a compatible non-Microsoft antivirus, Microsoft Defender Antivirus automatically turns itself off.
- Prefer an exclusion for one trusted file or folder over turning protection off.

## Verify
- [ ] Windows Security shows no current threats after the scan.

## Checked
Checked 2026-10-27 against Microsoft Support "Virus & threat protection in the Windows Security app" (Windows 11 and 10). Confirmed: section names, scan option descriptions, offline scan behaviour and results location, Allowed threats, real-time, cloud and tamper protection behaviour, Protection updates path, behaviour with third-party antivirus. Removed unconfirmed claims (scan durations, right-click Scan with Microsoft Defender, "passive mode" wording, scareware pop-up advice, repeat-detection advice).
Method: documentation only; no commands were run.
