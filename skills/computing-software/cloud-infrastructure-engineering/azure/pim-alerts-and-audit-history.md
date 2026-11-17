---
id: computing-software.cloud-infrastructure-engineering.azure.pim-alerts-and-audit-history
name: pim-alerts-and-audit-history
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, entra-id, pim, pim-alerts, pim-audit, audit-history, resource-audit, my-audit, roles-activated-too-frequently, too-many-global-admins, roles-assigned-outside-pim, stale-activations, auditlogs-kql, sentinel-pim, pim-security-alerts, alert-settings]
level: practitioner
status: docs-checked
description: "Use PIM security alerts (too many Global Admins, roles assigned outside PIM, frequent activations) and audit history; export to Log Analytics and query activation events."
sources: ["https://learn.microsoft.com/entra/id-governance/privileged-identity-management/pim-how-to-configure-security-alerts", "https://learn.microsoft.com/entra/id-governance/privileged-identity-management/pim-how-to-use-audit-log"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PIM alerts and audit history — see privilege drift before an auditor does

**Goal:** PIM's built-in alerts are tuned and triaged weekly, every activation and assignment
lands in Log Analytics, and the SOC has rules for the activations that matter.

## 1. Built-in PIM security alerts
PIM → Microsoft Entra roles (or Azure resources → subscription) → **Alerts**. Each alert has
a **Settings** gear (severity, threshold, enable/disable) and a **Fix** action.
| Alert | Trigger (configurable in alert settings) | Fix |
|---|---|---|
| Too many Global Administrators | Global Administrator assignments reach a threshold (2 to 100) and exceed a percentage of admins; both configurable, both must be met | Remove those who don't need it; assign lower roles |
| Roles are being assigned outside of PIM | a privileged role assigned outside PIM | Remove the assignment; prohibit that path |
| Roles are being activated too frequently | same user activates the same role N times (2 to 100) within a configurable period | Lengthen the role's activation duration |
| Administrators aren't using their privileged roles | no activation for a set number of days (0 to 100) | Remove from the role |
| Roles don't require MFA for activation | role setting without MFA | Require MFA for every role |
| Potential stale accounts in a privileged role | no sign-in for n days (1 to 365, configurable) | Remove from the role |
Review them in the weekly identity-ops meeting.

## 2. Audit history inside PIM
- **Resource audit** (Entra roles / per subscription): every assign, activate, deactivate,
  approve, role-setting change with requester, target, justification, ticket. Filter by
  time (data is available for the past 30 days), export CSV.
- **My audit**: the signed-in user's own PIM history — point auditors and the user here.
- Azure resources → subscription → **Resource audit** includes activations on child scopes.

## 3. Export to Log Analytics (the version that keeps > 30 days)
Entra ID → Diagnostic settings → send `AuditLogs` (and `SignInLogs`) to the workspace
(Azure Monitor diagnostic settings can also route it to a storage account). Azure
resource PIM events are in the subscription Activity log — add an Activity log
diagnostic setting too.
```kusto
// Entra role activations, last 7 days
AuditLogs
| where TimeGenerated > ago(7d)
| where OperationName has "Add member to role"
| extend Role = tostring(TargetResources[0].displayName), Actor = tostring(InitiatedBy.user.userPrincipalName)
| project TimeGenerated, Actor, Role, OperationName, ResultDescription
// Global Admin activations -> alert rule
AuditLogs
| where OperationName has "Add member to role" and TargetResources has "Global Administrator"
// all events of one activation: take roleAssignmentRequestId from the first query's AdditionalDetails
AuditLogs
| where AdditionalDetails has "<roleAssignmentRequestId>"
```
Create a log-search alert (severity 1) on the last query; a Sentinel analytics rule with entity
mapping Account ← `InitiatedBy.user.userPrincipalName` gives you incidents with the user's
other activity.

## 4. Review cadence
- Weekly: PIM alerts blade; activations per user per role (spot the `Contributor` activated daily → candidate for a lower role).
- Monthly: `roleEligibilitySchedules` export diffed against last month (new eligibility is an audit finding if no ticket).
- Quarterly: access review on each privileged role (PIM → Access reviews), auto-apply results.

## Gotchas
- PIM blade audit covers only the past 30 days; route it to Log Analytics or storage for longer retention.
- CorrelationId can differ across the asynchronous steps of one activation; correlate with `roleAssignmentRequestId` in AdditionalDetails.

## Verify
- [ ] PIM Alerts blade shows 0 open high-severity alerts (or each has an owner and a ticket).
- [ ] `AuditLogs | where OperationName has "Add member to role" | summarize max(TimeGenerated)` shows a test activation.
- [ ] The Global Admin activation alert fires (test with a break-glass-adjacent test role, not the real break-glass account).

## Checked

2026-10-28. Confirmed against Microsoft Learn pages: alert triggers and ranges (Global Administrator threshold 2 to 100, stale accounts 1 to 365 days, unused role 0 to 100 days, frequent activation 2 to 100), 30-day audit availability, diagnostic-settings export, the Add member to role AuditLogs query and roleAssignmentRequestId correlation.

Removed because not confirmed: the Duplicate role alert, 15 minute latency, Sentinel rule names, AzureActivity query, LoggedByService and ActivityDisplayName values, and per-scope threshold claim.

Method: documentation only; no commands were run.
