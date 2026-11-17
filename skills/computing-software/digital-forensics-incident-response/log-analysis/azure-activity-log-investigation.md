---
id: computing-software.digital-forensics-incident-response.log-analysis.azure-activity-log-investigation
name: azure-activity-log-investigation
category: computing-software
field: digital-forensics-incident-response
product: log-analysis
tags: [azure-activity-log, azure, cloud-forensics, control-plane, dfir]
level: practitioner
status: docs-checked
description: "Investigate Azure control-plane activity with the Activity Log: scope, fields, 90-day retention, az CLI retrieval and export to Log Analytics, storage or Event Hubs."
sources: ["https://learn.microsoft.com/en-us/azure/azure-monitor/essentials/activity-log", "https://learn.microsoft.com/en-us/azure/azure-monitor/essentials/activity-log-schema"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Azure Activity Log investigation

The Activity Log records Azure Resource Manager (control-plane) operations. It does not capture data-plane operations such as getting a secret from a key vault or making a request to a database: those are in resource logs, which are not collected by default and need a diagnostic setting.

## Retention and preservation
- Azure keeps activity log events for 90 days and then deletes them. To keep them longer, create a diagnostic setting that sends them to a Log Analytics workspace, Azure Storage or Azure Event Hubs, ideally before an incident. The page notes resource creator information is one of the main reasons to extend retention, because it is only available in the activity log.
- In Log Analytics the data is in the `AzureActivity` table; retention can be extended up to 12 years, and there is no ingestion charge for the activity log. String values in `AzureActivity` can differ in case, so compare with `=~` or `tolower()`.
- Retrieval with the CLI (start and end of the range must both fall within the 90-day window):
```bash
az monitor activity-log list --start-time "<START>" --end-time "<END>" -o json > activity.json
az monitor activity-log list --offset 14d       # relative range
```
`--max-events` limits the number of records returned.

## Scopes
Subscription-level events are the default scope. Tenant-level and management-group-level events capture only Azure Resource Manager events in those hierarchies (for example management group or subscription creation, policy assignments, management group membership changes) and can duplicate subscription events. The management-group queries need the `2017-03-01-preview` REST API version.

## Fields to read
From the schema page: `caller` (for example a user principal name), `claims` (including `ipaddr` and `appid`), `callerIpAddress`, `operationName`, `status`, `resourceId`, `correlationId` (groups related events; you can filter by it in REST), and `properties`, which can include `requestbody`.

## Verify
Each suspicious operation is tied to an identity whose sign-in logs explain the access, and the log range you queried falls inside the retention window or an exported copy.

## Checked
Checked 2026-11-09 against the Microsoft Learn Activity log page (scope, 90-day retention, diagnostic settings destinations, AzureActivity, az CLI options, tenant and management group scopes) and the activity log event schema page (caller, claims, correlationId, resourceId, operationName, status, properties.requestbody). Removed: the high-value operation table and KQL filter, the `az ad sp show` tip, and the claim that tenant and management-group operations are in the Entra audit log (the page says they are activity log events); the 30-day `az` example with a fixed date.
Method: documentation only; no commands were run.
