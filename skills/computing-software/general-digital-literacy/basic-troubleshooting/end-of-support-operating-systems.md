---
id: computing-software.general-digital-literacy.basic-troubleshooting.end-of-support-operating-systems
name: end-of-support-operating-systems
category: computing-software
field: general-digital-literacy
product: basic-troubleshooting
tags: [basic-troubleshooting, updates, end-of-support, windows-10-end-of-support, extended-security-updates, unsupported-os, upgrade-windows-11, windows-11-upgrade]
level: intro
status: docs-checked
description: "Recognise when an OS stops getting security updates (Windows 10 ended 14 Oct 2025) and choose between Windows 11, consumer ESU to Oct 2027, or a new PC."
sources:
  - https://support.microsoft.com/en-us/windows/deployment/updates-lifecycle/windows-10-support-has-ended-on-october-14-2025
  - https://learn.microsoft.com/en-us/lifecycle/products/windows-10-home-and-pro
  - https://support.microsoft.com/en-us/windows/experience/compatibility/windows-11-system-requirements
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# End-of-support operating systems

**Goal:** don't keep using a device online after it stops receiving security fixes.

## What end of support means
Microsoft says that after end of support a Windows PC still works, but it no longer gets technical support, software updates, or security updates or fixes, so it is at greater risk from viruses and malware.

## Windows 10
- **Windows 10 reached end of support on 14 October 2025.** Version 22H2 was the final version of Windows 10 (Home and Pro).
- Microsoft's options: upgrade to Windows 11 if the PC is eligible; get a new Windows 11 PC; or enrol in the **Windows 10 Consumer Extended Security Updates (ESU)** program, which Microsoft says can protect a Windows 10 device until **12 October 2027**. Microsoft recommends ESU for PCs that cannot run Windows 11. See Microsoft's end-of-support page for the enrolment steps.
- **Free upgrade:** only PCs running Windows 10 version 22H2 that meet the minimum hardware requirements can upgrade. Check eligibility in Settings > Update & Security > Windows Update > Check for updates, or with the **PC Health Check** app.
- **Windows 11 minimum requirements** include a 1 GHz or faster CPU with 2 or more cores on Microsoft's approved CPU list, 4 GB RAM, 64 GB storage, UEFI with Secure Boot capability, TPM 2.0, a DirectX 12 compatible graphics card with a WDDM 2.0 driver, and a 720p display larger than 9 inches. Home and personal-use Pro editions need internet and a Microsoft account at first setup.
- To move files and settings to a new PC, Microsoft points to **Windows Backup**.
- Microsoft 365 apps on Windows 10 get security updates for three years after Windows 10 end of support (to 10 October 2028), but Microsoft still recommends Windows 11.

## Other systems
For a Mac, phone or tablet, check the maker's own support page for how long the model receives security updates.

## Old computer
Microsoft encourages trade-in and recycling programs from retailers and PC makers, including its own trade-in program for eligible devices.

## Verify
- [ ] Each device's OS version is still supported (or enrolled in ESU), with its end date noted.

## Checked
Checked 2026-10-27 against Microsoft Support "Windows 10 support has ended on October 14, 2025", Microsoft Lifecycle "Windows 10 Home and Pro" and Microsoft Support "Windows 11 System Requirements". Confirmed: end-of-support date and meaning, final version, consumer ESU end date (12 October 2027), free upgrade conditions, hardware requirements, Microsoft 365 date, Windows Backup. Removed unconfirmed claims (winver command, "about the current and two previous macOS versions", iPhone and Android update lengths, ChromeOS Flex and Linux options, ESU enrolment path through Windows Update).
Method: documentation only; no commands were run.
