---
id: computing-software.systems-network-administration.patch-management.patch-compliance-reporting-by-group
name: patch-compliance-reporting-by-group
category: computing-software
field: systems-network-administration
product: patch-management
tags: [patch-compliance-report, patch-verification, compliance-reporting, configmgr-reports, intune-reports, patch-management]
level: practitioner
status: docs-checked
description: "Report patch compliance by device group using ConfigMgr software update reports and alerts and Intune feature update reports, with data latency and unsupported-OS blind spots."
sources:
  - https://learn.microsoft.com/en-us/mem/configmgr/sum/deploy-use/monitor-software-updates
  - https://learn.microsoft.com/en-us/mem/intune/protect/windows-update-reports
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Patch compliance reports by group

**Goal:** one report that shows, per group and tier, how many systems are on the current baseline and which are behind, from the platform's own reports.

## Working definitions (your own policy, not vendor wording)
Decide before reporting what counts as compliant, non-compliant and unknown (no recent report from the device), and count unknown separately so broken agents do not look like success.

## ConfigMgr
- Software Updates Dashboard: Monitoring > Overview > Security > Software Updates Dashboard shows device compliance and which devices are at risk.
- Per-update drill-down: Software Library > Software Updates > All Software Updates, pick an update required by at least one device, Summary tab, "View Required" link. That opens a temporary Devices node where you can create a collection from the list.
- Reports: more than 30 predefined software update reports, plus custom reports. Useful ones named on the page:
  - Compliance 9 - Overall health and compliance (version 1806 and later): healthy vs total clients in a collection, compliance pie for a software update group, top 5 non-compliant updates by article ID.
  - Management 2 - Updates required but not deployed.
  - Troubleshooting 2 - Deployment errors (errors at the site with a count of computers per error).
- Deployment status: Monitoring > Overview > Deployments, select the software update group or update, View Status. From version 2107 you can right-click a status and choose Evaluate Software Update Deployments.
- Alerts: set a compliance percentage threshold in the ADR or in the deployment; alerts show in the Software Library Software Updates node and the Monitoring Alerts node.
- Blind spot: devices running an unsupported operating system display as compliant because no updates apply to them any more. Cross-check OS versions separately.

## Intune (feature update policies)
- Reports > Windows Updates > Windows Feature Update Report (organizational, per policy: choose a profile, Generate report, refine by update status and ownership), and Devices > Monitor > Feature update failures (operational, alerts per policy with recommended actions).
- Columns include Update State, Update Substate, Update Aggregated Status, Last Scan Time, Target Version and Last Event Time.
- Latency: service-side Windows Update data typically arrives in under an hour; client-side data is batched, refreshes every eight hours, and exists only after you configure data collection. Client-side states replace server-side ones when available.
- Failure alerts the page lists include DiskFull, PolicyConflictDeferral, PolicyConflictPause, SafeguardHold (see the Windows release health dashboard), EndOfService and FailureResponseThreshold. Several (WUDamaged, WUComponentMissing, InstallIssue) point to `dism /online /cleanup-image /restorehealth`.
- These reports cover feature update policies only and their data is not used in other Intune reports.

## Report layout (suggested)
| Group | Tier | In scope | Compliant | Non-compliant | Unknown | Oldest missing update |
|---|---|---|---|---|---|---|
Plus a drill-down list of non-compliant devices with owner and missing items, and a fixed cutoff date so months compare.

## Verify
Totals for each group reconcile with your asset inventory's in-scope count, and a spot-checked non-compliant device is genuinely missing the listed update.

## Checked
Date: 2026-11-07. Read in full: Monitor software updates in Configuration Manager (dashboard, drill-through, alerts, deployment status, report names, unsupported-OS note) and Intune "Reports for feature update policies" (latency, report paths, columns, state definitions, alert message table). Removed as unconfirmed: the NIST SP 800-40 source and all claims attributed to it, SQL view `v_UpdateComplianceStatus`, `Get-WsusComputer` usage, Windows Update for Business reports in Log Analytics, Linux Satellite/Landscape/Ansible counting, the 30-day aging bucket, and the CMDB reconciliation practice (kept only as a generic verify step).
Method: documentation only; no commands were run.
