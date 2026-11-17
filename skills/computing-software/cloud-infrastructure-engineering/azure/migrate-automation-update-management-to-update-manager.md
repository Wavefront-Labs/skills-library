---
id: computing-software.cloud-infrastructure-engineering.azure.migrate-automation-update-management-to-update-manager
name: migrate-automation-update-management-to-update-manager
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, update-manager, update-management-migration, automation-update-management, mma-retirement, maintenance-configuration]
level: practitioner
status: docs-checked
description: "Move from retired Automation Update Management to Azure Update Manager: migration tooling, schedules to maintenance configurations, pre/post events, agent removal."
sources: ["https://learn.microsoft.com/azure/update-manager/guidance-migration-automation-update-management-azure-update-manager", "https://learn.microsoft.com/azure/update-manager/migration-overview", "https://learn.microsoft.com/azure/update-manager/pre-post-scripts-overview"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Migrate Automation Update Management to Update Manager

**Goal:** finish the move off Automation Update Management without
losing patch schedules.

## Map the concepts
| Automation Update Management | Azure Update Manager |
|---|---|
| Software update configuration (schedule) | Maintenance configuration (scope InGuestPatch) |
| Saved search / dynamic groups | Dynamic scopes |
| Pre/post scripts (runbooks) | Pre/post **events** via Event Grid (handlers such as webhooks and Functions) |
| Periodic assessment | Periodic assessment checks for updates every 24 hours; enforce at scale with Azure Policy |

## Migration steps
1. Follow the Azure Update Manager migration guide for Automation Update Management: recreate each schedule as a maintenance configuration (InGuestPatch scope) with dynamic scopes.
2. Non-Azure machines: onboard to Azure Arc first.
3. Rebuild pre/post scripts as pre/post events (Event Grid on the maintenance configuration).
4. Run both side by side for one cycle with the old schedules disabled after verification - not both active (double patching).
5. Remove old software update configurations and the Updates solution once the new schedules are verified.

## Gotchas
- Reports built on the old Update Management data stop; rebuild them on Update Manager data.
- Linux machines with custom pre-scripts that stopped services need equivalent automation in post events.

## Verify
- [ ] Every former schedule has a maintenance configuration with matching window and scope; first cycle installs updates.

## Checked

Date: 2026-10-28.

Confirmed against Learn (Update Manager overview, scheduled patching, pre/post events): maintenance configurations with dynamic scopes, Event Grid pre and post events with webhook and Function handlers, periodic assessment every 24 hours enforceable with Azure Policy.
Removed: the 12-hour assessment figure, retirement date, migration-tool behaviour, Customer Managed Schedules/patchMode property names, event type names, Update/UpdateSummary table names and MMA removal details (not on fetched pages).

Method: documentation only; no commands were run.
