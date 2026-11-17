---
id: computing-software.cloud-infrastructure-engineering.azure.update-manager-for-arc-enabled-servers
name: update-manager-for-arc-enabled-servers
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, update-manager, update-manager-arc, azure-arc, hybrid-patching, maintenance-configuration]
level: practitioner
status: docs-checked
description: "Patch on-prem and multicloud servers with Azure Update Manager through Arc: prerequisites, periodic assessment policy, schedules, pricing exemptions and limitations."
sources: ["https://learn.microsoft.com/azure/update-manager/overview", "https://learn.microsoft.com/azure/update-manager/update-manager-faq", "https://learn.microsoft.com/azure/update-manager/assessment-options"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Update Manager for Arc-enabled servers

**Goal:** one patching tool and one compliance view for Azure VMs and every Arc-connected server.

## Prerequisites
- Server connected to Azure Arc, with access to its update source (Windows Update/WSUS, or Linux package repositories).

## Assessment
- Enable **periodic assessment** (every 24 hours) at scale with Azure Policy.
- On demand: portal *Check for updates*, or
```bash
az connectedmachine assess-patches -g rg-hybrid -n srv-db01
```

## Patching
- One-time: `az connectedmachine install-patches -g rg-hybrid -n srv-db01 --maximum-duration PT2H --reboot-setting IfRequired --windows-parameters classificationsToInclude="Critical" "Security"`
- Scheduled: maintenance configuration (scope InGuestPatch) assigned to Arc machines directly or via dynamic scopes
  - same as Azure VMs.

## Cost
Update Manager is at no extra charge for Azure VMs and for Arc-enabled Azure Local VMs created through the Arc resource bridge. Other Arc-enabled servers are charged unless covered, for example by Extended Security Updates enabled by Arc or Defender for Servers Plan 2 on the subscription; see the Update Manager pricing page and FAQ.

## Gotchas
- Check the FAQ for how machines fetch updates from WSUS (Windows) and private repositories (Linux).
- Check the supported-systems list for OS versions before onboarding.

## Verify
- [ ] All Arc servers show assessment within 24 h; a test schedule installs updates and reports in update history.

## Checked

Date: 2026-10-28.

Confirmed against Learn (Update Manager FAQ, overview, scheduled patching): periodic assessment every 24 hours enforceable via Azure Policy, maintenance configurations with dynamic scopes, no extra charge for Azure VMs and Arc-enabled Azure Local VMs, ESU and Defender for Servers Plan 2 coverage, WSUS and private repository question covered in the FAQ. `az connectedmachine` commands via check_commands.py.
Removed: azcmagent check, agent and Automation account statements, Arc patch orchestration limit, hotpatching note, WSUS approval and Event Grid statements (not on fetched pages).

Method: documentation only; no commands were run.
