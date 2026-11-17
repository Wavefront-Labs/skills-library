---
id: computing-software.cloud-infrastructure-engineering.azure.azure-functions-patterns
name: azure-functions-patterns
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, azure-functions, serverless, faas, flex-consumption, consumption-plan, premium-plan, elastic-premium, dedicated-plan, isolated-worker-model, triggers, bindings, service-bus-trigger, event-hubs-trigger, event-grid, durable-functions, fan-out-fan-in, retry-policy, poison-queue, dead-letter, idempotency, cold-start, always-ready, managed-identity, identity-based-connections, host-json, vnet-integration]
level: practitioner
status: docs-checked
description: "Build reliable Azure Functions: pick Flex Consumption vs Premium vs Dedicated, trigger retry and poison semantics, host.json concurrency, identity-based connections and Durable Functions patterns."
sources: ["https://learn.microsoft.com/en-us/azure/azure-functions/functions-scale", "https://learn.microsoft.com/en-us/azure/azure-functions/flex-consumption-plan", "https://learn.microsoft.com/en-us/azure/azure-functions/functions-bindings-error-pages", "https://learn.microsoft.com/en-us/azure/azure-functions/functions-reliable-event-processing", "https://learn.microsoft.com/en-us/azure/azure-functions/functions-concurrency", "https://learn.microsoft.com/en-us/azure/azure-functions/event-driven-scaling", "https://learn.microsoft.com/en-us/azure/azure-functions/manage-connections", "https://learn.microsoft.com/en-us/azure/durable-task/durable-functions/durable-functions-overview", "https://learn.microsoft.com/en-us/azure/durable-task/common/durable-task-storage-providers"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Azure Functions patterns — plan, triggers, retries and orchestration

**Goal:** functions on a plan that matches their latency and networking needs, with
known retry and poison-message behaviour per trigger, no connection strings, and
multi-step work in Durable Functions instead of ad-hoc chaining.

## 1. Choose the hosting plan
| Plan | Use for | Notes |
|---|---|---|
| **Flex Consumption** | Recommended for new serverless apps | Scale to zero, VNet integration, **always-ready** instances for faster cold starts, Linux only |
| Consumption | Legacy | Linux Consumption is retired; Windows Consumption is the legacy plan (migrate to Flex) |
| Elastic Premium | Long runs, heavy VNet use, Windows or Linux, predictable latency | Pre-warmed instances |
| Dedicated (App Service plan) | Spare App Service capacity, or full control | Scale with App Service plan autoscale |
| Container Apps | Function apps alongside containers | Scaling managed by the Container Apps environment |
Timeouts: Consumption default 5 min, max 10 min; Flex and Premium enforce no maximum;
HTTP-triggered functions must respond within 230 seconds regardless of the timeout setting (Azure Load Balancer idle timeout) — use
async request-reply (Durable HTTP API) for long HTTP work.

## 2. Use the isolated worker model
Support for the .NET in-process model ends on November 10, 2026. New .NET apps use the **isolated worker** model; Flex Consumption does not support the in-process model. Use the current programming model for each language.

## 3. Know each trigger's failure semantics
- **Queue Storage:** up to 5 attempts (`maxDequeueCount`, default 5), then the message moves to a poison queue. Alarm on poison queue length.
- **Service Bus:** message is abandoned on exception; after `MaxDeliveryCount` (default 10)
  it goes to the **dead-letter** subqueue. Lock duration must exceed processing time, or
  enable auto-renew (`maxAutoLockRenewalDuration`).
- **Event Hubs / Cosmos DB change feed / Kafka:** checkpoint-based — a failed batch is
  **not** redelivered unless you configure a **retry policy** (function-level, for example the
  `FixedDelayRetry` or `ExponentialBackoffRetry` attributes); otherwise the checkpoint advances past
  the failed batch. Catch per-event errors and write failures to a side queue yourself.
- **Event Grid:** retries with backoff up to 24 h / 30 attempts, then dead-letter to a
  blob container **only if** you configured one on the subscription.
- All of these are at-least-once: make handlers **idempotent** (dedupe on message ID in
  Table/Cosmos with a TTL, or use Service Bus duplicate detection at the sender).

## 4. Tune concurrency in host.json
```json
{"version": "2.0",
 "concurrency": {"dynamicConcurrencyEnabled": true, "snapshotPersistenceEnabled": true},
 "extensions": {"serviceBus": {"maxConcurrentCalls": 16, "prefetchCount": 0},
                "queues": {"batchSize": 16, "newBatchThreshold": 8}}}
```
Cap scale-out with `functionAppScaleLimit` (Elastic Premium) or the Flex
maximum instance count to protect databases.

## 5. No secrets: identity-based connections
Replace `AzureWebJobsStorage` and trigger connection strings with
`<CONNECTION>__fullyQualifiedNamespace` / `AzureWebJobsStorage__accountName` settings plus
a managed identity granted the data roles (e.g. *Azure Service Bus Data Receiver*,
*Storage Blob Data Owner* + *Storage Queue Data Contributor* for the host storage).
Key Vault references (`@Microsoft.KeyVault(SecretUri=...)`) for anything that must remain a secret.

## 6. Durable Functions for workflows
Patterns: **function chaining**, **fan-out/fan-in** (`Task.WhenAll` over activities),
**async HTTP API**, **monitor**, **human interaction** (wait for external event with
timer), **aggregator** (durable entities).
- Orchestrator code must be **deterministic**: no `DateTime.Now`, random, direct I/O
  or non-durable awaits — use `context.CurrentUtcDateTime`, activities and durable timers.
- Long histories slow replay; use `ContinueAsNew` for eternal orchestrations.
- Storage backends: Azure Storage, Netherite, MSSQL, or the **Durable Task Scheduler** managed backend, which the docs list as the recommended option (check region availability with `az provider show --namespace Microsoft.DurableTask`).

## Gotchas
- Changing an orchestrator's code while instances are in flight breaks replay — version orchestrations (new name) instead.
- VNet-integrated apps need the host storage account reachable (private endpoints for the `file`, `blob` and `table` subresources, plus `queue` for Durable Functions) or the host won't start.

## Verify
- [ ] Plan chosen with a stated reason; cold-start sensitive functions have always-ready/pre-warmed instances.
- [ ] Each trigger has a documented failure path (poison queue, DLQ, retry policy or side queue) with an alert.
- [ ] Replaying a message twice yields one side effect.
- [ ] App settings contain no connection strings or keys; identities hold least-privilege data roles.
- [ ] Orchestrators pass a determinism review and survive a host restart mid-run.

## Checked
Checked 2026-10-24 against azure-docs azure-functions pages (functions-scale, flex-consumption-plan, migrate-dotnet-to-isolated-model, functions-bindings-storage-queue(-trigger), functions-bindings-service-bus(-trigger), functions-bindings-error-pages, functions-reliable-event-processing, functions-concurrency, event-driven-scaling, manage-connections, configure-networking-how-to) and the Durable Task docs (overview, storage providers, scheduler, code constraints). Confirmed: Flex Linux only; Consumption 5 and 10 minute timeouts, no maximum on Flex and Premium; 230 s HTTP limit; queue maxDequeueCount 5; Service Bus max delivery count 10 and 5 minute default auto lock renewal; host.json concurrency and extension settings shown; Event Hubs and Kafka retry policies are function-level; Event Grid retry 24 h and 30 attempts; functionAppScaleLimit; in-process support ends November 10, 2026; Durable Task Scheduler recommended; orchestrators use CurrentUtcDateTime. Found stale and fixed: Linux Consumption described as being retired (it is retired) and Consumption as the Y1 plan. Removed unconfirmed: per-function scaling, minimum billed instance, read-only run-from-package claim, partition-bound scaling statement.

Method: documentation only; no commands were run.
