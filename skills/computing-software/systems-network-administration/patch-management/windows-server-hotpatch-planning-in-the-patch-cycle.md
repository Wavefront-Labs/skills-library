---
id: computing-software.systems-network-administration.patch-management.windows-server-hotpatch-planning-in-the-patch-cycle
name: windows-server-hotpatch-planning-in-the-patch-cycle
category: computing-software
field: systems-network-administration
product: patch-management
tags: [hotpatch, patch-management, windows-server, reboot-planning, azure-arc]
level: practitioner
status: docs-checked
description: "Plan a hotpatch-based Windows Server patch cycle: baseline versus hotpatch months, supported platforms, reboot calendar and rollback handling."
sources: ["https://learn.microsoft.com/en-us/windows-server/get-started/hotpatch"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hotpatch in the patch cycle

**Goal:** fewer reboots without losing patch coverage. Companion to `computing-software.systems-network-administration.windows-server.hotpatch-for-windows-server`, which holds the enablement steps.

## How the calendar works
Hotpatch first establishes a baseline with the current Cumulative Update. Every three months the baseline refreshes with the latest Cumulative Update, and the next two months get Hotpatch releases (if January is a Cumulative Update, February and March are Hotpatch releases). Hotpatch updates do not require a restart.
- Planned baselines come on a regular cadence (for example four baselines and eight Hotpatch releases in a year), include everything in the comparable Latest Cumulative Update and require a restart.
- Unplanned baselines replace a Hotpatch month when an important update, such as a zero-day fix, cannot be released as a Hotpatch. They also require a restart and cannot be predicted in advance.
- Use the Windows Server Hotpatch Calendar linked from the Microsoft page for the actual schedule.

## Supported platforms (check the page for the current list)
- Azure and Azure Local VMs: only the listed publisher, offer and SKU combinations for Windows Server 2022 and 2025 Azure Edition images; custom images and container base images are not supported.
- Azure Arc-connected machines: Windows Server 2025 Datacenter or Standard, with the feature enabled in the Azure Arc portal. The page says Arc-enabled Hotpatch for Windows Server 2025 is available at no extra cost.

## Planning
1. Inventory hosts: hotpatch eligible versus not; group by service tier.
2. Treat baseline months as maintenance windows with a restart; use Hotpatch months for light-touch rollout (rings still apply).
3. Orchestration depends on platform: Azure VMs have Automatic VM Guest Patching enabled by default (Critical and Security patches, applied in off-peak hours of the VM time zone); Arc-connected machines can use Azure Update Manager, Group Policy, SConfig (Server Core) or non-Microsoft tools.
4. Plan restarts for what Hotpatch does not cover: nonsecurity Windows updates, .NET updates, and non-Windows updates such as drivers and firmware must still be installed with a restart in Hotpatch months. Also restart periodically after a new baseline to stay in sync with nonsecurity patches.
5. Plan rollback: Hotpatch updates do not support automatic rollback. If there is a problem you uninstall the latest update and install the last functional baseline update, which requires restarting the VM.

## Gotchas
Patches you install manually in Azure do not follow availability-first principles and might require a restart.

## Verify
`Get-HotFix` in PowerShell (or Settings in Desktop Experience) shows installed patches. In the Azure portal, VM Overview, Operations, Updates shows Hotpatch status and recent patches; the Update compliance tab lists available patches not auto-installed.

## Checked
Date: 2026-11-07. Read in full: Hotpatch for Windows Server (How Hotpatch works, planned and unplanned baselines, supported platforms table, supported updates, patch orchestration per platform, patch status in Azure, rollback). Corrected: the page says Arc-enabled Hotpatch for Windows Server 2025 is at no extra cost (the draft said licensed as a subscription feature); supported platforms include Windows Server 2022 Azure Edition images and Arc-connected Server 2025 Standard/Datacenter. Removed as unconfirmed: virtualization-based security prerequisite, the January/April/July/October month list (page gives only the three-month cadence and a January example), "hosts that missed a baseline cannot take hotpatches", silent fallback, third-party agents, snapshot advice, Update Manager "maintenance configurations".
Method: documentation only; no commands were run.
