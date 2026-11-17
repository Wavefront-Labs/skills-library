---
id: computing-software.systems-network-administration.windows-server.azure-update-manager-for-servers
name: azure-update-manager-for-servers
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, azure-arc, azure-update-manager, maintenance-configuration, periodic-assessment, patch-orchestration, dynamic-scope, windows-updates, servicing]
level: practitioner
status: docs-checked
description: "Patch Azure and Arc-enabled Windows servers with Azure Update Manager: periodic assessment, maintenance configurations with dynamic scopes, pre/post events and reporting."
sources:
  - https://learn.microsoft.com/en-us/azure/update-manager/overview
  - https://learn.microsoft.com/en-us/azure/update-manager/scheduled-patching
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Azure Update Manager for Windows servers

**What:** Azure's patch assessment and scheduling for Azure VMs and Arc-enabled servers; it has no dependency on Log Analytics or Azure Automation. See the vendor's pricing page for costs.

## Assessment
Enable **periodic assessment** (checks for updates every 24 hours); results appear under Update Manager > Machines.

## Scheduled patching
1. Create a **maintenance configuration**: scope *Guest (Azure VM, Arc-enabled VMs/servers)*,
   recurrence, maintenance window (maximum 3 hours 55 minutes), reboot setting, update classifications,
   include/exclude KBs.
2. Assign machines: static list, or **dynamic scope** by subscription/RG/location/OS/tags
   (for example by tag).
3. Azure VMs need patch orchestration set to **Customer Managed Schedules**.

## Gotchas
- Window too short: installs stop at the window end; large CUs on slow servers need time.

## Verify
- [ ] All servers show recent assessment.
- [ ] Last scheduled run succeeded for each wave; reboot status clean.

## Checked
2026-10-28: Confirmed on Learn pages update-manager/overview and scheduled-patching: no dependency on Log Analytics or Azure Automation, periodic assessment every 24 hours, maintenance configurations, 3 hours 55 minutes maximum window, Customer Managed Schedules requirement, dynamic scopes, Arc-enabled servers supported. Removed: pricing and licence-coverage sentence, retirement claim, built-in policy name, patchMode property values, Event Grid events, wave schedule, Resource Graph query, WSUS gotcha, reboot-setting default.
Method: documentation only; no commands were run.
