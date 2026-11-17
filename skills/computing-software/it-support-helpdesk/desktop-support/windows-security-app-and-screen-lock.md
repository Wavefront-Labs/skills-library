---
id: computing-software.it-support-helpdesk.desktop-support.windows-security-app-and-screen-lock
name: windows-security-app-and-screen-lock
category: computing-software
field: it-support-helpdesk
product: desktop-support
tags: [it-support-helpdesk, desktop-support, windows-security-app, screen-lock, defender-health, lock-screen, endpoint-security]
level: practitioner
status: docs-checked
description: "Use the Windows Security app for scans and real-time protection, and enforce screen lock with the machine inactivity limit policy or Intune compliance."
sources:
  - "https://support.microsoft.com/en-us/windows/stay-protected-with-windows-security-2ae0363d-0ada-c064-8b56-6a39afb6a963"
  - "https://learn.microsoft.com/en-us/windows/security/threat-protection/security-policy-settings/interactive-logon-machine-inactivity-limit"
  - "https://learn.microsoft.com/en-us/mem/intune/protect/compliance-policy-create-windows"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# windows-security-app-and-screen-lock

## Windows Security app
- Built into Windows 10 and 11; open it by searching for Windows Security in the Start menu. It covers Microsoft Defender Antivirus, Windows Firewall and Smart App Control.
- Scan one file or folder: right-click it in File Explorer, Scan with Microsoft Defender (on Windows 11 select Show more options first).
- Quick scan when malware is suspected: Virus & threat protection > Quick scan.
- Real-time protection toggle: Virus & threat protection > Manage settings. While off, opened or downloaded files are not scanned; it turns back on automatically soon after.

## Screen lock
- Group Policy / security policy: Interactive logon: Machine inactivity limit (Computer Configuration\Windows Settings\Security Settings\Local Policies\Security Options). Value is seconds of inactivity, 0 to 599,940; 0 or blank disables it, so sessions never lock. Client default is Disabled. Needs a restart to take effect.
- The session locks by invoking the screen saver, which should be active on the machine. With this policy set, the device also locks when the screen saver starts or the display turns off from power settings.
- Choose the time by device use and location: a short limit in public areas, longer where a trusted group uses the device and lock hurts productivity.
- Intune Windows compliance policy, Password section: "Maximum minutes of inactivity before password is required" sets the idle time before the user must re-enter the password.

## Verify
The device locks itself after the configured inactivity time, and the policy value shows in Security Options (or the Intune compliance policy).

## Checked
Date: 2026-11-09. Confirmed in the three Microsoft pages: Windows Security app tasks, the machine inactivity limit policy (location, range, disabled values, default, restart, screen saver behaviour, best practice) and the Intune compliance password inactivity setting. Removed as unconfirmed: the tile table, Get-MpComputerStatus properties, Update-MpSignature, Dynamic Lock, the Intune settings catalog name, macOS and mobile guidance, Tamper Protection and physical-security habits.
Method: docs-checked 2026-11-09 against the three Microsoft pages listed in sources, downloaded and read (compliance page by targeted search).
