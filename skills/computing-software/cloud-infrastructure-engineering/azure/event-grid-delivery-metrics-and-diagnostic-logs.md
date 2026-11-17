---
id: computing-software.cloud-infrastructure-engineering.azure.event-grid-delivery-metrics-and-diagnostic-logs
name: event-grid-delivery-metrics-and-diagnostic-logs
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, event-grid, eg-metrics, delivery-failures, dead-lettering, diagnostic-settings]
level: practitioner
status: docs-checked
description: "Monitor Event Grid with publish and delivery metrics, failed-delivery diagnostic logs, dead-letter storage and alerts so dropped events are noticed."
sources: ["https://learn.microsoft.com/en-us/azure/event-grid/delivery-and-retry", "https://learn.microsoft.com/en-us/azure/event-grid/monitor-push-reference", "https://learn.microsoft.com/en-us/azure/event-grid/enable-diagnostic-logs-topic", "https://learn.microsoft.com/en-us/azure/event-grid/manage-event-delivery", "https://learn.microsoft.com/en-us/azure/azure-monitor/reference/tables/aegdeliveryfailurelogs", "https://learn.microsoft.com/en-us/cli/azure/eventgrid/event-subscription"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Event Grid monitoring

**Goal:** know when events fail to publish or deliver, and keep the failures for replay.

## Metrics (per topic, filter by subscription)
| Metric | Watch for |
|---|---|
| Published Events / Publish Failed Events | Publisher errors (auth, size, schema) |
| Matched Events / Unmatched Events | Filters dropping events unexpectedly |
| Delivered Events / Delivery Failed Events | Destination failing |
| Delivery Failed Events (`DeliveryAttemptFailCount`; dimensions `Error`, `ErrorType`) | What the destination returned |
| Dead Lettered Events / Dropped Events | Final failure: kept (dead-letter) or lost (dropped) |
| Destination Processing Duration | Slow handlers causing timeouts |

**Dropped Events > 0 means data loss** (dead-lettering not configured, or the dead-letter destination was not found): alert on it.

## Retry and dead-letter
- Default retry policy: maximum 30 attempts (allowed 1-30) and event time-to-live 1440 minutes (allowed 1-1440), whichever limit is reached first, with exponential backoff; configure `--max-delivery-attempts` and `--event-ttl`.
- Configure dead-letter to a blob container: `az eventgrid event-subscription create ... --deadletter-endpoint <storageId>/blobServices/default/containers/deadletter`.
- Not retried (dead-lettered, or dropped if dead-lettering is off): 400, 413 and 403 for Azure resource endpoints; 400, 413, 401 and 403 for webhooks. A 401 from an Azure resource endpoint is retried after 5 minutes or more.

## Diagnostic logs
Diagnostic settings categories `DeliveryFailures` and `PublishFailures` (and `DataPlaneRequests`, audit traces of data plane operations). In a Log Analytics workspace the delivery failures land in the `AegDeliveryFailureLogs` table:
```kusto
AegDeliveryFailureLogs
| where TimeGenerated > ago(1d)
| summarize count() by EventSubscriptionName, Message = substring(Message, 0, 150)
```

## Alerts
- Delivery Failed Events > 0 for 15 min per subscription.
- Dropped Events > 0 (severity 1).
- Dead-letter container blob count increasing (Storage metric or Event Grid on the container itself).

## Verify
- [ ] Break a test subscription endpoint, confirm DeliveryFailures log entries, dead-letter blob created, alert fires.

## Checked
Checked 2026-10-24 against azure-docs Event Grid pages (delivery-and-retry, monitor-push-reference, enable-diagnostic-logs-topic, manage-event-delivery) and the azure-docs-cli eventgrid reference. Confirmed: metric REST names PublishSuccessCount, PublishFailCount, MatchedEventCount, UnmatchedEventCount, DeliverySuccessCount, DeliveryAttemptFailCount (Error and ErrorType dimensions), DeadLetteredCount, DroppedEventCount, DestinationProcessingDurationInMs; default max attempts 30 and TTL 1440 minutes; 30 s response timeout; dead-letter endpoint resource ID format; AegDeliveryFailureLogs table and its EventSubscriptionName and Message columns. Fixed: the non-retry list (403 for Azure resources, 401 is retried for them) and the DataPlaneRequests description.

Method: documentation only; no commands were run.
