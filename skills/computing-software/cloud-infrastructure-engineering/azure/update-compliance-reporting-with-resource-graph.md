---
id: computing-software.cloud-infrastructure-engineering.azure.update-compliance-reporting-with-resource-graph
name: update-compliance-reporting-with-resource-graph
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, update-manager, patchassessmentresources, update-compliance-report, resource-graph, patch-reporting]
level: practitioner
status: gated
description: "Report patch compliance across Azure VMs and Arc servers with Resource Graph patchassessmentresources and patchinstallationresources, workbooks and alerts."
sources: ["https://learn.microsoft.com/azure/update-manager/query-logs", "https://learn.microsoft.com/azure/update-manager/sample-query-logs", "https://learn.microsoft.com/azure/update-manager/workbooks"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Update compliance reporting with Resource Graph

**Goal:** a reliable "which machines are missing critical/security patches, and did last night's run work?" report.

## Tables
- `patchassessmentresources`: latest assessment per machine (`.../patchAssessmentResults`) and each missing patch
  (`.../softwarePatches`).
- `patchinstallationresources`: installation runs (`.../patchInstallationResults`) and per-patch results.
Update Manager keeps the most recent assessment history for the last 7 days and installation history for the last
30 days in Resource Graph; export for longer history.

## Machines missing critical/security updates
```kusto
patchassessmentresources
| where type !has "softwarepatches"
| extend p = properties.availablePatchCountByClassification, os = tostring(properties.osType)
| extend critical = toint(p.critical), security = toint(p.security)
| where critical > 0 or security > 0
| project machine = tostring(split(id, "/patchAssessmentResults")[0]), os, critical, security,
          lastAssessed = todatetime(properties.lastModifiedDateTime)
| order by critical desc
```

## Stale assessments (blind spots)
```kusto
patchassessmentresources
| where type !has "softwarepatches"
| where todatetime(properties.lastModifiedDateTime) < ago(2d)
| project id, last = properties.lastModifiedDateTime
```

## Failed installations last 24 h
```kusto
patchinstallationresources
| where type !has "softwarepatches"
| where todatetime(properties.lastModifiedDateTime) > ago(1d)
| extend status = tostring(properties.status)
| where status != "Succeeded"
| project id, status, started = properties.startDateTime, error = properties.errorDetails
```
Check the exact `status` values against the property table in the query-logs page before alerting on them
(gated: unconfirmed, source is paywalled or blocked).

## Present it
- Update Manager workbooks (the Azure Workbooks feature): clone and extend with the queries above.
- Export on a schedule to storage if you need audit evidence beyond the retention above.

## Gotchas
- Machines without periodic assessment never appear: pair with an inventory join (`resources` vs assessments).
- Classification keys in `availablePatchCountByClassification` include critical, security, updates and other (see the
  sample query page); check which apply per OS before building totals.

## Verify
- [ ] Report count of machines equals inventory count; known-unpatched test VM appears with correct counts.

## Checked
2026-10-28. Confirmed (Learn: update-manager/query-logs, sample-query-logs): table names, `availablePatchCountByClassification`,
`lastModifiedDateTime`, `osType`, `startDateTime`, `errorDetails`, the `type !has "softwarepatches"` filter pattern, 7-day
assessment and 30-day installation history. Corrected: retention was stated as 7 days for everything. Removed: the Linux
Security/Other claim, `arg("")` alert and Logic App export steps. Gated: the `status` value "Succeeded" (not seen in the
fetched text).
Method: documentation only; no commands were run.
