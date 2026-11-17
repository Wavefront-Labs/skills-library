---
id: computing-software.systems-network-administration.windows-server.hotpatch-for-windows-server
name: hotpatch-for-windows-server
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, windows-server-installation, hotpatch, rebootless-updates, baseline-month, azure-edition, azure-arc, windows-server-2025, servicing, reboot-management, azure-update-manager]
level: practitioner
status: verified
description: "Use Windows Server hotpatching (Azure Edition VMs and Arc-connected Server 2025): baseline vs hotpatch months, what still needs reboots, orchestration tools, rollback and planning."
sources:
  - https://learn.microsoft.com/en-us/windows-server/get-started/hotpatch
aliases:
  - computing-software.systems-network-administration.patch-management.windows-server-hotpatch
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Hotpatch for Windows Server

**What:** Hotpatch installs Windows security updates by patching the in-memory code of running processes, so the machine does not restart. Microsoft refreshes a **baseline** cumulative update every three months (restart required) and ships **hotpatch** updates for the following two months. A planned year therefore has four baselines and eight hotpatch releases: about 4 reboots a year instead of 12.

Checked 2026-10-18 against Microsoft Learn "Hotpatch for Windows Server" (updated 2026-09-08). This skill merges the earlier `patch-management.windows-server-hotpatch` skill (kept as an alias).

## Where it is available
- **Azure and Azure Local virtual machines** created from the listed marketplace images only: `2022-Datacenter-Azure-Edition-Core`, `-Core-smalldisk`, `-Hotpatch`, `-Hotpatch-smalldisk`, and `2025-Datacenter-Azure-Edition`, `-smalldisk`, `-Core`, `-Core-smalldisk` (publisher MicrosoftWindowsServer, offer WindowsServer). Container base images, custom images and other SKU combinations are not supported.
- **Azure Arc-connected machines**: Windows Server 2025 **Standard** or **Datacenter**, with Hotpatch enabled in the Azure Arc portal. Microsoft's page states Arc-enabled Hotpatch for Windows Server 2025 is available at no extra cost (earlier it was a paid subscription: check current terms).
- Not covered by this model: Windows client hotpatch (Windows 11 Enterprise 24H2 through Autopatch/Intune), which is separate.
- Azure Virtual Machine Scale Sets with Uniform orchestration cannot be created on Azure Edition hotpatch images.

## Cadence
- Baseline: the current cumulative update for that quarter; **requires a restart**. Example from Microsoft: if January is a baseline, February and March are hotpatch releases. Use Microsoft's Windows Server Hotpatch Calendar for the actual months.
- **Unplanned baselines** (for example a zero-day that cannot ship as a hotpatch) replace a hotpatch month and require a restart.
- Hotpatches cover **Windows security updates only**, with parity to the regular security content.

## What still needs a restart
In hotpatch months you must still restart for: non-security Windows updates, .NET updates, and non-Windows updates such as drivers and firmware. A machine also needs the periodic baseline restart so it stays in sync with non-security patches.

## Orchestration
- **Azure VMs**: Automatic VM Guest Patching is on by default for supported images; it installs Critical and Security patches in off-peak hours (VM time zone) using availability-first principles. Patches you install manually do not follow availability-first and may need a restart.
- **Azure Local**: Group Policy for Windows Update client settings, SConfig on Server Core, or third-party patch tools.
- **Arc-connected machines**: Azure Update Manager, Group Policy, SConfig or third-party tools.
- Check installed patches with `Get-HotFix` or Settings; the Azure portal VM Updates blade shows Hotpatch status.

## Rollback
Hotpatch updates do not support automatic rollback. If one causes a problem you must uninstall the latest update and install the last working baseline, which requires a restart.

## Planning
- Book reboot windows for baseline months and unplanned baselines; keep normal change control for the hotpatch months.
- Track baseline compliance: a machine must be on the current baseline to receive that quarter's hotpatches.
- Prerequisites such as virtualization-based security were not stated on the Learn hotpatch page: confirm the requirements for your platform in the Azure Update Manager hotpatch documentation before enrolling.

## Verify
- Azure Update Manager (or the VM Updates blade) shows the machine as hotpatch-enabled and the last update as a hotpatch with no pending restart.
- Uptime (`(Get-CimInstance Win32_OperatingSystem).LastBootUpTime`) is unchanged across a hotpatch month while `Get-HotFix` lists the new security update.
