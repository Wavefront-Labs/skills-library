---
id: computing-software.cloud-infrastructure-engineering.azure.service-bus-monitoring-metrics-and-throttling
name: service-bus-monitoring-metrics-and-throttling
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, service-bus, sb-monitoring, sb-metrics, active-messages, dead-lettered-messages, sb-throttling, server-busy, namespace-cpu, messaging-units, alerts, runtime-audit-logs]
level: practitioner
status: docs-checked
description: "Monitor Azure Service Bus: active/dead-lettered/scheduled message metrics per entity, throttling (ServerBusy), Premium CPU/memory per MU, logs, and alerts that catch stuck consumers."
sources: ["https://learn.microsoft.com/en-us/azure/service-bus-messaging/monitor-service-bus", "https://learn.microsoft.com/en-us/azure/service-bus-messaging/monitor-service-bus-reference", "https://learn.microsoft.com/en-us/azure/service-bus-messaging/service-bus-throttling", "https://learn.microsoft.com/en-us/azure/service-bus-messaging/service-bus-premium-messaging", "https://learn.microsoft.com/en-us/azure/service-bus-messaging/service-bus-quotas", "https://learn.microsoft.com/en-us/azure/azure-monitor/reference/supported-metrics/microsoft-servicebus-namespaces-metrics", "https://learn.microsoft.com/en-us/azure/service-bus-messaging/automate-update-messaging-units"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Service Bus monitoring — backlog, dead letters and throttling

**Goal:** know when consumers stop keeping up, when poison messages pile into DLQs, and when the
namespace itself (not your code) is the limit — with alerts per queue/subscription.

## 1. Metrics that matter (dimension `EntityName`)
| Metric | Meaning | Alert idea |
|---|---|---|
| `ActiveMessages` | ready to receive (backlog) | growing for 15 min, or > N for this queue |
| `DeadletteredMessages` | in the DLQ | > 0 (critical queues) or increase over 1 h |
| `ScheduledMessages` | future-dated | sanity checks only |
| `IncomingMessages` / `OutgoingMessages` / `CompleteMessage` | throughput in/out | out ≪ in sustained = consumers behind |
| `ThrottledRequests` | requests rejected (ServerBusy) | > 0 sustained |
| `ServerErrors` / `UserErrors` | service vs client faults | spikes |
| `NamespaceCpuUsage` / `NamespaceMemoryUsage` (Premium) | namespace CPU and memory percent (dimension `Replica`) | sustained high → add MUs |
| `Size` | entity bytes | near the entity's configured max size (1 GB to 80 GB) |
```bash
az monitor metrics alert create -g rg-msg -n sb-orders-dlq --scopes <namespace-id> \
  --condition "max DeadletteredMessages > 0 where EntityName includes orders" --window-size 15m --evaluation-frequency 5m --severity 2 --action <ag-id>
az servicebus queue show -g rg-msg --namespace-name sb-prod -n orders --query "countDetails"   # active, deadLetter, scheduled, transferDeadLetter
```
Metrics use a one-minute grain and message counts are point-in-time values; `countDetails` returns the counts from the management API.

## 2. Logs
Diagnostic settings → Log Analytics: `OperationalLogs` (management ops), `VNetAndIPFilteringLogs`,
`RuntimeAuditLogs` (Premium only; aggregated data-plane operations such as send and receive, with auth type and key), and `DiagnosticErrorLogs` (client-side, throttling and quota-exceeded errors). Use resource-specific tables (AZMSOperationalLogs, AZMSVnetConnectionEvents, AZMSRunTimeAuditLogs, AZMSDiagnosticErrorLogs).
```kusto
AZMSRuntimeAuditLogs | where TimeGenerated > ago(1h) and Status != "Success"
| summarize count() by ActivityName, AuthKey, ClientIP, Status
```

## 3. Throttling
- **Standard**: credit-based throttling shared with other tenants; server busy errors
  once credits run out; the SDK retry policy backs off exponentially. Mitigate by batching, fewer management ops, or Premium. A per-entity limit of 5,000 concurrent receive requests also returns server busy.
- **Premium**: dedicated **messaging units** (1, 2, 4, 8 or 16); throttling is driven by the namespace's CPU and memory limits —
  scale MUs (manual, or autoscale rules on CPU or memory) and spread hot entities across namespaces.
- Client SDK retries handle transient busy errors; log them as warnings, alert on rate.

## 4. Triage stuck consumers
- Backlog rising + `OutgoingMessages` ~ 0 → consumers down or failing auth (check `UserErrors`, RuntimeAuditLogs).
- Backlog rising + high `AbandonMessage`/deliveries + DLQ growth → poison messages; inspect DLQ
  (`DeadLetterReason`, `DeadLetterErrorDescription`) via Service Bus Explorer and resubmit after fix.
- Lock lost errors → processing longer than `LockDuration`; renew locks or increase duration.

## Gotchas
- Namespace-level alerts without `EntityName` hide a single stuck queue among healthy ones.
- Subscriptions each have their own DLQ — alert per subscription for topics.
- Auto-forwarding chains report counts on the final entity; `TransferDeadLetter` counts failures in the forward.
- Metrics don't show message age; add consumer-side lag metrics (enqueued time vs processed time).

## Verify
- [ ] Alerts exist per critical entity for backlog, DLQ > 0 and throttling; Premium has CPU/memory alerts or autoscale.
- [ ] Stopping a non-prod consumer fires the backlog alert within the window.
- [ ] Runtime/operational logs flow to the workspace and are queryable by identity.

## Checked
Checked 2026-10-24 against the azure-docs Service Bus pages (monitor-service-bus-reference, service-bus-throttling, service-bus-quotas and its limits include, service-bus-premium-messaging, automate-update-messaging-units) and the Azure Monitor supported-metrics page for Microsoft.ServiceBus/Namespaces. Confirmed: REST metric names (ActiveMessages, DeadletteredMessages, ScheduledMessages, IncomingMessages, OutgoingMessages, CompleteMessage, AbandonMessage, ThrottledRequests, ServerErrors, UserErrors, Size, NamespaceCpuUsage, NamespaceMemoryUsage) and the EntityName dimension; PT1M grain; runtime audit logs Premium-only with ClientIP, AuthKey, ActivityName and Status columns; credit-based Standard throttling; 1, 2, 4, 8, 16 messaging units; 1 GB to 80 GB entity size. Removed unconfirmed: the 70 percent CPU threshold, the fixed 10 s back-off, the ApplicationMetricsLogs description.

Method: documentation only; no commands were run.
