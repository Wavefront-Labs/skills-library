---
id: computing-software.digital-privacy-hygiene.device-hardening.cleaning-an-infected-computer
name: cleaning-an-infected-computer
category: computing-software
field: digital-privacy-hygiene
product: device-hardening
tags: [digital-privacy-hygiene, device-hardening, malware-removal, malware, malware-protection, microsoft-defender-offline, reinstall-windows, browser-hijacker, adware, second-opinion-scanner]
level: practitioner
status: draft
description: "Decide between cleaning and reinstalling after a malware infection, run Defender Offline and second-opinion scans, remove browser hijacks, and rotate credentials afterwards."
sources:
  - "https://ssd.eff.org/module/how-do-i-protect-myself-against-malware"
  - "https://support.microsoft.com/en-us/windows/help-protect-my-pc-with-microsoft-defender-offline-9306d528-64bf-4668-5b80-ff533f183d6c"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Cleaning an infected computer

**Goal:** get back to a trustworthy machine. "Trustworthy" usually means reinstall.

## Decide: clean or rebuild
| Infection | Approach |
|---|---|
| Adware, browser hijacker, unwanted toolbar | Clean is usually enough |
| Infostealer, RAT, remote-access scam tool, ransomware, rootkit, unknown | **Back up data, wipe, reinstall** |
| Can't tell | Rebuild |

## Cleaning steps (Windows)
1. Disconnect from the network.
2. Windows Security > Virus & threat protection > Scan options > **Microsoft Defender
   Antivirus (offline scan)** (reboots and scans before Windows loads).
3. Second opinion: Malwarebytes free scanner or ESET Online Scanner.
4. Settings > Apps: uninstall unknown/recent programs; check `Startup apps` and Task
   Scheduler for odd entries.
5. Browsers: reset settings (Chrome Settings > Reset settings), remove extensions,
   check `chrome://policy` for injected policies; check search engine and home page.
macOS: remove unknown login items/profiles (System Settings > General > Login Items;
Privacy & Security > Profiles), run Malwarebytes for Mac.

## Rebuild steps
1. Copy **documents/photos only** to external media (no executables, no installers).
2. Reinstall: Windows "Reset this PC" with **cloud download** + remove everything, or USB
   media; macOS Recovery erase and reinstall.
3. Install apps fresh from official sources; scan restored files.

## Afterwards
From a clean device: rotate passwords, revoke sessions and tokens (see
`computing-software.digital-privacy-hygiene.password-hygiene.responding-to-infostealer-credential-theft`).

## Verify
- [ ] Offline scan and second-opinion scan clean (or OS reinstalled).
- [ ] Credentials rotated after the machine was clean.
