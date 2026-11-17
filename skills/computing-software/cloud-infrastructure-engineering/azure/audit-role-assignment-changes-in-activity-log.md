---
id: computing-software.cloud-infrastructure-engineering.azure.audit-role-assignment-changes-in-activity-log
name: audit-role-assignment-changes-in-activity-log
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, azure-rbac, role-assignment-audit, rbac-change-log, azureactivity, activity-log-alerts, security-monitoring]
level: practitioner
status: docs-checked
description: "Answer who granted what access and when: read role assignment writes/deletes in the activity log, query them in Log Analytics and read the key fields."
sources: ["https://learn.microsoft.com/azure/role-based-access-control/change-history-report", "https://learn.microsoft.com/azure/azure-monitor/essentials/activity-log-schema", "https://learn.microsoft.com/azure/azure-monitor/alerts/alerts-create-activity-log-alert-rule"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Audit role assignment changes

**Goal:** a reliable trail of RBAC changes, kept longer than the activity log window.

## What is logged
Role assignment and role definition changes in your subscriptions are logged in the Azure Activity Log, and you can view the past 90 days there. Logged operations: create role assignment, delete role assignment, create or update custom role definition, delete custom role definition. Portal filters: Event category = Administrative, plus the Operation.

Key fields of an entry:
- `authorization:action`: `Microsoft.Authorization/roleAssignments/write` (create), `.../roleAssignments/delete`, `Microsoft.Authorization/roleDefinitions/write`, `.../roleDefinitions/delete`.
- `authorization:scope`, `caller` (user or an object ID when a service principal made the change), `eventTimestamp`, `status:value` (Started, Succeeded, Failed).
- A write entry with a `requestbody` property carries `PrincipalId`, `PrincipalType`, `RoleDefinitionId` and `Scope`.

## Quick look
```bash
az monitor activity-log list --namespace "Microsoft.Authorization" --start-time 2021-03-01 --offset 7d
az monitor activity-log list --namespace "Microsoft.Authorization" --start-time 2021-03-01 --offset 7d --query '[].{authorization:authorization, caller:caller, eventTimestamp:eventTimestamp, properties:properties}'
```
Replace the example start date with your own. PowerShell equivalent: `Get-AzLog -StartTime (Get-Date).AddDays(-7) | Where-Object {$_.Authorization.Action -like 'Microsoft.Authorization/roleAssignments/*'}`.

## Long-term: Azure Monitor logs
Send the activity log to a Log Analytics workspace (Azure Monitor logs lets you write complex queries, integrate with alerts and Power BI, keep data longer and cross-reference other logs). Queries from Microsoft's page:
```kusto
AzureActivity
| where TimeGenerated > ago(60d) and Authorization contains "Microsoft.Authorization/roleAssignments/write" and ActivityStatus == "Succeeded"
| parse ResourceId with * "/providers/" TargetResourceAuthProvider "/" *
| summarize count(), makeset(Caller) by TargetResourceAuthProvider
```
```kusto
AzureActivity
| where TimeGenerated > ago(60d) and Authorization contains "Microsoft.Authorization/roleAssignments"
| summarize count() by bin(TimeGenerated, 1d), OperationName
| render timechart
```

## Alerts
Create an activity log alert rule (see the Learn page "Create or edit an activity log, service health, or resource health alert rule"; it has a Status field for choosing the status levels) and pair it with the Learn article "Alert on privileged Azure role assignments" for filtering on high-privilege roles. The built-in Owner role definition GUID is `8e3af657-a8ff-443c-a75c-2fe8c4bcb635`.

## Verify
- [ ] The query returns a test assignment you just created.

## Checked

Method: docs-checked 2026-11-09 against the Learn pages change-history-report (read in full), activity-log-schema (keyword check for status values) and the Owner role GUID in the role-assignments-template page. Removed unconfirmed claims: management-group-scope log placement, the Success operationNameValue KQL, ID-resolution commands, the User Access Administrator GUID, the PIM service principal note and the Entra audit log note.
