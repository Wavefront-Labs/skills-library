---
id: computing-software.cloud-infrastructure-engineering.azure.storage-metrics-resource-logs-and-storage-insights
name: storage-metrics-resource-logs-and-storage-insights
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, storage-accounts, storage-insights, storagebloblogs, storage-metrics, throttling, latency]
level: practitioner
status: docs-checked
description: "Monitor Azure Storage: key metrics and dimensions, E2E vs server latency, resource logs to StorageBlobLogs, KQL for 403s and top callers, and Storage insights."
sources: ["https://learn.microsoft.com/azure/storage/blobs/monitor-blob-storage", "https://learn.microsoft.com/azure/azure-monitor/reference/supported-metrics/microsoft-storage-storageaccounts-blobservices-metrics", "https://learn.microsoft.com/azure/azure-monitor/reference/tables/storagebloblogs", "https://learn.microsoft.com/azure/storage/common/storage-insights-overview"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Storage metrics, logs and insights

**Goal:** explain slow or failing storage access with data, and alert before users notice.

## Metrics
| Metric | Split by | Use |
|---|---|---|
| Transactions | ResponseType, ApiName, Authentication | Count requests by response type to see errors and throttling |
| SuccessE2ELatency vs SuccessServerLatency | ApiName | Large gap = client/network side slowness |
| Availability | ApiName | Percentage of availability for the service or API |
| Ingress / Egress | | Throughput vs scalability targets |
| BlobCapacity, BlobCount | BlobType, Tier | Capacity (time grains of one hour or longer) |
The transaction metrics have a one-minute time grain; the capacity metrics are one hour or longer, so don't alert on them at minute granularity.
Alert candidates: Availability below your target, Transactions split by ResponseType for server-side and throttling errors, SuccessE2ELatency above baseline.

## Resource logs
Diagnostic settings are per service **sub-resource** (blobServices/default, queueServices/default, ...):
Create a diagnostic setting on the blob service (and the other services you use) with the log categories you need and a Log Analytics workspace, storage account or event hub as destination; see the Azure Monitor documentation for the category list.
Blob service logs land in the `StorageBlobLogs` table (queue, table and file services have their own tables).
```kusto
// Who is getting 403?
StorageBlobLogs
| where TimeGenerated > ago(1h) and StatusCode == "403"
| summarize count() by CallerIpAddress, AuthenticationType, StatusText, RequesterObjectId
// Top callers by egress
StorageBlobLogs | summarize egressGB = sum(ResponseBodySize)/1e9 by CallerIpAddress | top 10 by egressGB
```
Sending logs to Log Analytics is billed; choose categories and destinations (for example a storage account with a lifecycle policy for retention) with cost in mind.

## Storage insights
Azure Monitor > Insights > Storage accounts: workbook across accounts for availability, latency, failures, capacity.

## Gotchas
- `AuthenticationType` in logs records the authentication used (for example `AccountKey`, `SAS`) - use it before disabling shared key.
- Capacity metrics have time grains of an hour or more; don't alert on minute granularity.

## Verify
- [ ] Logs flowing for all used services; alerts tested; dashboard shows E2E vs server latency per API.

## Checked

2026-10-24, against the Azure Monitor reference for Microsoft.Storage/storageAccounts/blobServices metrics (generated 2026-07-31) and the StorageBlobLogs table (2026-08-14): metric names Transactions, SuccessE2ELatency, SuccessServerLatency, Availability, Ingress, Egress, BlobCapacity, BlobCount and their dimensions and time grains (one minute for transaction metrics, one hour or longer for capacity); StorageBlobLogs columns CallerIpAddress, AuthenticationType, StatusCode, StatusText, RequesterObjectId, ResponseBodySize, OperationName, TlsVersion. Removed the unconfirmed ClientThrottlingError, ServerBusyError and AuthorizationError names, UsedCapacity, the claim that metrics are free, the legacy classic-analytics remark and the per-service log table names other than StorageBlobLogs. Removed the diagnostic-settings CLI example because its category names were not confirmed.

Method: documentation only; no commands were run.
