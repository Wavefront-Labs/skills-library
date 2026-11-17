---
id: computing-software.systems-network-administration.patch-management.patch-deployment-success-rate
name: patch-deployment-success-rate
category: computing-software
field: systems-network-administration
product: patch-management
tags: [patch-success-rate, deployment-success, patch-metrics, kpi, patch-management]
level: practitioner
status: draft
description: "Measure patch deployment success rate correctly: denominator choice, first-attempt vs eventual success, failure categorisation, and queries for ConfigMgr, Intune, SSM and Ansible."
sources:
  - https://learn.microsoft.com/en-us/mem/configmgr/sum/deploy-use/monitor-software-updates
  - https://docs.aws.amazon.com/systems-manager/latest/userguide/patch-manager-compliance-reports.html
  - https://csrc.nist.gov/pubs/sp/800/40/r4/final
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Patch deployment success rate

## Definition
`success rate = devices that installed all targeted updates in the window / devices targeted that were online and healthy`

Report alongside it:
- **Reach** = devices targeted / devices in inventory (catches out-of-scope or unhealthy agents).
- **First-attempt success** vs **eventual success** (after retries) - first-attempt shows pipeline quality.
- **Failure categories**: download, install error code, reboot pending, offline, insufficient disk, user deferred, pre-check failed.

## Sources
- ConfigMgr: Deployment Status (Success/In Progress/Error/Requirements not met/Unknown); SQL `v_UpdateDeploymentSummary`/`v_AssignmentState_Combined`.
- Intune/WUfB reports: Windows Update for Business reports in Log Analytics (`UCClientUpdateStatus` with `ClientState`, `UpdateInstalledTime`).
- AWS SSM: `aws ssm list-compliance-summaries --filters Key=ComplianceType,Values=Patch`; per-run `list-command-invocations` status.
- Ansible: callback plugin output or AWX job host summaries (ok/changed/failed/unreachable).

Example Kusto (WUfB reports):
```kusto
UCClientUpdateStatus
| where TimeGenerated > ago(1d) and UpdateCategory == "WindowsQualityUpdate"
| summarize total=dcount(AzureADDeviceId), ok=dcountif(AzureADDeviceId, ClientState=="Installed") by TargetBuild
| extend pct = round(100.0*ok/total,1)
```

## Targets
- First-attempt success >= 95% per wave; eventual >= 99% by deadline.
- Any error code over 1% of devices gets a root-cause ticket.

## Gotchas
- Excluding offline devices from the denominator flatters the number; report them separately and age them.
- "Requirements not met" in ConfigMgr often means the update is not applicable; exclude these from failures but verify.
- A single wave with a broken update skews monthly averages; show per-wave numbers.

## Verify
Success rate published per wave with the denominator and top 5 failure codes; trend reviewed in the monthly patch report.
