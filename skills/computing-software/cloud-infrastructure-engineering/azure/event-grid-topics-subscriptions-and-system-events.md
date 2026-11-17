---
id: computing-software.cloud-infrastructure-engineering.azure.event-grid-topics-subscriptions-and-system-events
name: event-grid-topics-subscriptions-and-system-events
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, event-grid, event-subscriptions, event-grid-topics, system-topics, custom-topics, partner-topics, event-domains, event-grid-namespaces, mqtt-broker, pull-delivery, push-delivery, cloudevents, event-schema, event-filtering, advanced-filters, dead-lettering, retry-policy, webhook-validation, event-handlers, managed-identity-delivery, blob-events, resource-events, event-driven-architecture]
level: practitioner
status: docs-checked
description: "Wire event-driven flows with Event Grid: system/custom/partner topics, domains, namespaces with pull delivery and MQTT, CloudEvents, advanced filters, retries and dead-lettering, identity delivery."
sources: ["https://learn.microsoft.com/en-us/azure/event-grid/delivery-and-retry", "https://learn.microsoft.com/en-us/azure/event-grid/event-filtering", "https://learn.microsoft.com/en-us/azure/event-grid/quotas-limits", "https://learn.microsoft.com/en-us/azure/event-grid/system-topics", "https://learn.microsoft.com/en-us/azure/event-grid/end-point-validation-event-grid-events-schema", "https://learn.microsoft.com/en-us/azure/event-grid/managed-service-identity", "https://learn.microsoft.com/en-us/azure/event-grid/authenticate-with-microsoft-entra-id", "https://learn.microsoft.com/en-us/azure/event-grid/event-schema-key-vault", "https://learn.microsoft.com/en-us/azure/event-grid/concepts-event-grid-namespaces", "https://learn.microsoft.com/en-us/azure/storage/blobs/storage-blob-event-overview", "https://learn.microsoft.com/en-us/cli/azure/eventgrid"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Event Grid — route events from Azure and your apps to handlers, with retries you understand

**Goal:** things that happen (blob created, VM deleted, order placed, secret expiring)
become events delivered at least once to the right handler with filters at the
broker, dead-lettered when they can't be delivered, and never lost because a
webhook was down for an hour.

## 1. Which topic
| Source | Topic type |
|---|---|
| Azure resources (Storage blobs, Key Vault, Resource groups/subscriptions, Container Registry, Service Bus, IoT Hub, Maps, Communication Services, Update Manager, Policy, Health…) | **System topic** (one per source resource; created implicitly by the first subscription or explicitly) |
| Your application events | **Custom topic** (one endpoint, your schema) |
| Many tenants/customers with isolated topics under one umbrella | **Event domain** (thousands of topics, publish once, domain-level auth) |
| SaaS partners (Auth0, SAP, Tribal, Microsoft Graph change notifications) | **Partner topic** |
| Queue-like pull consumption, MQTT devices, CloudEvents-native | **Event Grid namespace** (namespace topics with **pull delivery** or push to Event Hubs; **MQTT broker**) |
```bash
az eventgrid system-topic create -g rg -n st-stprod-blob --source <storage-account-id> --topic-type Microsoft.Storage.StorageAccounts --location uksouth --identity systemassigned
az eventgrid system-topic event-subscription create -g rg --system-topic-name st-stprod-blob -n to-ingest \
  --endpoint-type servicebusqueue --endpoint <sb-queue-id> --delivery-identity systemassigned --delivery-identity-endpoint-type servicebusqueue --delivery-identity-endpoint <sb-queue-id> \
  --included-event-types Microsoft.Storage.BlobCreated --subject-begins-with "/blobServices/default/containers/raw/blobs/incoming/" --subject-ends-with ".parquet" \
  --advanced-filter data.contentLength NumberGreaterThan 0 --event-delivery-schema cloudeventschemav1_0 \
  --max-delivery-attempts 30 --event-ttl 1440 --deadletter-identity systemassigned --deadletter-identity-endpoint <storage-container-id>
az eventgrid topic create -g rg -n egt-orders -l uksouth --input-schema cloudeventschemav1_0 --identity systemassigned --public-network-access disabled   # then a private endpoint; set disableLocalAuth=true via ARM to kill keys/SAS
```

## 2. Schemas and filtering
- Prefer **CloudEvents 1.0** (`specversion`, `type`, `source`, `id`, `time`, `subject`, `data`) for new topics and subscriptions — portable, and what namespace topics accept; the Event Grid schema uses `eventType`, `topic`, `subject`, `data`.
- Filters are evaluated at the broker: event type list, `subject` begins/ends with (blob path prefix is the classic), **advanced filters** on `data.*` (`StringContains`, `NumberIn`, `IsNullOrUndefined`, `StringNotBeginsWith`, arrays), limits: 25 advanced filters and 25 filter values across all filters per subscription, 512 characters per string value; array keys need `enableAdvancedFilteringOnArrays`.
- One subscription per handler; fan-out is free; put coarse filters in the subscription and fine logic in the handler.

## 3. Handlers and delivery
Handlers: Functions (`EventGridTrigger` — no validation dance), Webhooks (HTTPS), **Service Bus queues/topics**, **Event Hubs**, Storage Queues, Relay, Logic Apps, Container Apps/Apps via webhook, Event Grid namespace topics, Automation, and newer "Azure Monitor alerts" handlers.
- Push delivery: at-least-once; retries with exponential backoff up to `max-delivery-attempts` (default 30) or `event-ttl` (default 1 440 min); 400 and 413 are not retried (nor 403, and 401 for webhooks); an attempt is considered failed after 30 s without a response — handlers must **ack fast and process async** (enqueue, return 200). Batched delivery (`--max-events-per-batch`, `--preferred-batch-size-in-kilobytes`).
- **Dead-letter** to a blob container (`--deadletter-endpoint` + identity) — turn it on for every production subscription and alert on `DeadLetteredCount`.
- **Webhook validation**: Event Grid sends a `SubscriptionValidationEvent` with `validationCode` — respond with `{"validationResponse": "<code>"}` (synchronous) or do a GET on the `validationUrl` (manual); the request carries the `aeg-event-type: SubscriptionValidation` header. Logic Apps (Event Grid connector), Automation webhooks and Functions with the Event Grid trigger are validated automatically. Secure webhooks with Entra (`--azure-active-directory-tenant-id` and `--azure-active-directory-application-id-or-uri`).
- **Delivery with managed identity** (`--delivery-identity`) to Service Bus/Event Hubs/Storage: the topic's identity holds *Data Sender* on the destination — no connection strings, works with `disableLocalAuth` targets.
- Pull delivery (namespaces): consumers `receive` → `acknowledge`/`release`/`reject` with lock durations; MQTT v3.1.1/v5 broker with client certs/Entra, topic spaces and routing to namespace topics → Event Hubs/Functions.

## 4. Common patterns
- Blob ingestion: `BlobCreated` (filter `/containers/landing/blobs/`) → Service Bus queue (buffer) → Function/Container App; to avoid partial uploads filter on `data.api` for `CopyBlob`, `PutBlob`, `PutBlockList` or `FlushWithClose`, which fire only after data is fully committed.
- Governance: subscription-level system topic (`Microsoft.Resources.ResourceWriteSuccess`/`ResourceDeleteSuccess`) → Function that tags or notifies.
- Key Vault near-expiry (`Microsoft.KeyVault.SecretNearExpiry`) → rotation Function; Container Registry `ImagePushed` → deploy pipeline.
- App events: domain events published to a custom topic (CloudEvents, `type: com.example.orders.placed.v1`, `subject: /tenants/123/orders/456`), subscriptions per consumer with type filters, dead-letter to a shared container, consumers idempotent on `id`.

## 5. Security and ops
- Publish auth: Entra (*EventGrid Data Sender*; disable keys and SAS with the `disableLocalAuth` property) with managed identity, else SAS/keys (rotate); private endpoints (`privatelink.eventgrid.azure.net`) for topics/domains; inbound IP rules; service tag `AzureEventGrid` for outbound-to-handlers in NSGs.
- Metrics: `PublishSuccessCount`, `PublishFailCount`, `MatchedEventCount`, `DeliverySuccessCount`, `DeliveryAttemptFailCount` (by error), `DeadLetteredCount`, `DroppedEventCount` (TTL exceeded without dead-letter — the silent loss metric), `DestinationProcessingDurationInMs`; diagnostic logs `DeliveryFailures`, `PublishFailures`, `DataPlaneRequests`.
- Limits: 500 event subscriptions per topic (100 for event subscriptions at Azure subscription scope), 1 MB events (counted in 64 KB chunks), publish rate 5,000 events or 5 MB per second for custom and partner topics and domains.

## Gotchas
- Dead-lettering **off by default** — events that exhaust retries are **dropped**; `DroppedEventCount` is the first alert to create.
- Event Grid allows only **one** system topic per source; look for the existing one before creating (`az eventgrid system-topic list --query "[?source=='<id>']"`).
- `BlobCreated` also fires for REST calls that do not complete a blob; filter on `data.api` (`CopyBlob`, `PutBlob`, `PutBlockList`, `FlushWithClose`).
- Order of delivery is not guaranteed; sequence by `time`/your own sequence number in the handler.
- Webhook endpoints must complete the validation handshake when the subscription is created, so IaC must deploy the handler first (Functions with the Event Grid trigger, Logic Apps and Automation webhooks are validated automatically).

## Verify
- [ ] Every production event subscription has dead-lettering (`az eventgrid event-subscription show --query deadLetterWithResourceIdentity`) and an alert on `DeadLetteredCount`/`DroppedEventCount`.
- [ ] Upload a blob to the filtered prefix: event arrives in the Service Bus queue within seconds with `type Microsoft.Storage.BlobCreated` and CloudEvents envelope; a blob outside the prefix produces no event.
- [ ] Stop the handler for 10 minutes: `DeliveryAttemptFailCount` climbs, nothing is dropped, events flush on recovery in order of retry (not original order — handler tolerates it).
- [ ] Custom topic: publisher uses managed identity (no key in config); `PublishFailCount` 0; subscription filter on `type` delivers only the intended events.

## Checked
Checked 2026-10-24 against azure-docs Event Grid pages (delivery-and-retry, event-filtering and its filtering include, quotas limits include, system-topics, webhook endpoint validation, managed-service-identity, authenticate-with-microsoft-entra-id, event-schema-key-vault, concepts-event-grid-namespaces, monitor-push-reference), the Storage blob events overview and the azure-docs-cli eventgrid reference (all flags in the examples exist; there is no CLI flag for disabling local auth on topics). Confirmed: retry defaults (30 attempts, 1440 minutes), 30 s timeout, not-retried codes, dead-letter off by default, advanced filter limits and operator names, one system topic per source, 500 subscriptions per topic, 5,000 events or 5 MB per second publish rate, disableLocalAuth, EventGrid Data Sender, validationResponse handshake and automatic validation for Logic Apps, Automation and Functions, FlushWithClose guidance, SecretNearExpiry event. Found wrong and fixed: advanced filter limits (25 filters and 25 values total, not 5 per filter); non-retry codes. Removed unconfirmed: 5 minute validation window, Front Door/WAF behaviour, Update Manager and Policy event examples, _SUCCESS sentinel and Activity log comparison, missing-field filter behaviour, pricing statement.

Method: documentation only; no commands were run.
