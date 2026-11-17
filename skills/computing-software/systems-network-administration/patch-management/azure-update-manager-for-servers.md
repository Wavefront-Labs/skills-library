---
id: computing-software.systems-network-administration.patch-management.azure-update-manager-for-servers
name: azure-update-manager-for-servers
category: computing-software
field: systems-network-administration
product: patch-management
tags: [azure-update-manager, maintenance-configuration, azure-arc, periodic-assessment, windows-patch-tooling, linux-patching, azure]
level: practitioner
status: docs-checked
description: "Patch Azure VMs and Arc-enabled servers with Azure Update Manager: periodic assessment, maintenance configurations and dynamic scopes, patch orchestration modes and reporting."
sources:
  - https://learn.microsoft.com/en-us/azure/update-manager/overview
  - https://learn.microsoft.com/en-us/azure/update-manager/scheduled-patching
  - https://learn.microsoft.com/en-us/azure/update-manager/manage-update-settings
  - https://learn.microsoft.com/en-us/azure/update-manager/dynamic-scope-overview
  - https://learn.microsoft.com/en-us/azure/update-manager/pre-post-scripts-overview
  - https://learn.microsoft.com/en-us/cli/azure/maintenance/configuration
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Azure Update Manager for servers

**Goal:** one service to assess and patch Windows and Linux servers in Azure and on-premises (via Azure Arc). It does not depend on Log Analytics or Azure Automation.

## Assessment
Enable periodic assessment (Update Manager then fetches the latest updates for the machine every 24 hours) in the machine's update settings, or at scale with Azure Policy, so compliance data stays fresh.

## Scheduled patching
1. For Azure VMs, set patch orchestration to **Customer Managed Schedules**, which sets the patch mode to Azure-orchestrated (`AutomaticByPlatform`) and `BypassPlatformSafetyChecksOnUserSchedule` to true. This is not required for Arc-enabled machines.
2. Create a maintenance configuration (patch classifications are set with `--install-patches-windows-parameters` and `--install-patches-linux-parameters`):
```bash
az maintenance configuration create -g rg-patch --resource-name mc-prod-sat --maintenance-scope InGuestPatch --location westeurope --maintenance-window-start-date-time "2026-10-24 22:00" --maintenance-window-duration 03:55 --maintenance-window-recur-every "Month Fourth Saturday" --maintenance-window-time-zone UTC --reboot-setting IfRequired --extension-properties InGuestPatchMode=User
```
3. Assign machines directly or with **dynamic scopes** (see the dynamic scoping overview for the supported filters).

## Pre and post events
Update Manager uses Event Grid to create pre and post events on scheduled maintenance configurations; event handlers include Azure Webhooks and Azure Functions, for snapshots, load-balancer drain and health checks.

## Reporting
Portal views per machine and per update, or Azure Resource Graph:
```kusto
patchassessmentresources
| project id, properties.availablePatchCountByClassification
```

## Gotchas
- Update Manager is free for Azure VMs and for Azure Arc-enabled Azure Local VMs; for other Arc-enabled servers it is charged per server per month (see the Azure Update Manager pricing page).
- The upper maintenance window is 3 hours 55 minutes, and a reboot is skipped if too little of the window remains (10 to 15 minutes depending on machine type).

## Verify
After the window, the maintenance run history shows success per machine and the assessment shows no missing critical or security updates.

## Checked
Date: 2026-10-27. Documentation checked: Azure Update Manager overview, scheduled patching page (3 hours 55 minutes upper window, Customer Managed Schedules for Azure VMs, not required for Arc, reboot time rule), manage update settings page (Customer Managed Schedules sets Azure-orchestrated patch mode and BypassPlatformSafetyChecksOnUserSchedule), assessment options (24-hour periodic assessment), pre/post events page (Event Grid, webhooks, Functions), Azure Resource Graph tables page (`patchassessmentresources`, `availablePatchCountByClassification`), FAQ (pricing), `az maintenance configuration` reference (flags used; classification flags corrected, recur format "Month Fourth Saturday"). Removed the `az vm update` assessment command, the policy name, the retired-product statement, the WSUS note and the Resource Graph `type` filter, which were not confirmed. The previous prerequisite URL redirected to the dynamic scoping page and is replaced.

Method: documentation only; no commands were run.
