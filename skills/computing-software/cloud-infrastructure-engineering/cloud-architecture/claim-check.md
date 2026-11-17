---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.claim-check
name: claim-check
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, messaging-patterns, claim-check, large-messages, message-size-limit, object-storage, s3, blob-storage, sqs-extended-client, event-grid-blob-events]
level: practitioner
status: docs-checked
description: "Send large payloads through a queue by storing the body in object storage and passing a reference: limits per broker, lifecycle cleanup, access control and integrity."
sources: ["https://learn.microsoft.com/azure/architecture/patterns/claim-check", "https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/quotas-messages.html", "https://github.com/awslabs/amazon-sqs-java-extended-client-lib"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Claim check

**Trigger:** payloads exceed or approach the broker limit, or are large enough that messaging cost
and throughput suffer. Look up the current message-size limit of your broker (SQS quotas page, Service Bus
and Pub/Sub docs). Azure documents Service Bus Premium AMQP messages up to 100 MB, and the SQS Extended
Client library describes a 256 KB SQS limit; if the payload fits within a transport's limit without hurting
throughput or latency, send it inline.

## Steps
1. Producer writes the payload to object storage under an unguessable key and computes a content hash.
2. Producer sends a small message carrying the reference (bucket, key), hash, size and content type.
   Libraries can do this for you, such as the SQS Extended Client for Java.
3. Consumer fetches the object, verifies hash, processes, then acks.
4. **Cleanup**: define who owns payload deletion and coordinate message expiry with payload retention
   (lifecycle rule covering max message retention plus the DLQ redrive window), so a valid claim check never
   points at deleted data.
5. **Access**: consumers get read-only on the prefix and the store enforces access control independently of
   the broker. Prefer role-based access over pre-signed URLs in messages, since URLs can expire before a redrive.

## Variants
- Storage-event-triggered: the upload itself raises the event (Azure Event Grid `BlobCreated`); no producer message at all.
- Compress first, or use a more compact serializer, if the payload is only slightly over the limit.

## Gotchas
- Object store writes are not part of the message transaction; write object first, then send.
  Orphan objects from failed sends are cleaned by lifecycle.
- The payload now lives outside the broker with its own retention and access rules; classify both.

## Checked
2026-10-28. Confirmed against the Azure Claim Check pattern page (reference token, lifecycle ownership, integrity hash, store-side access control, availability, compression and splitting alternatives, Service Bus Premium 100 MB) and the SQS Extended Client README (256 KB). Removed: the per-broker limit list (SNS, Pub/Sub, Kafka, EventBridge, SQS 1 MiB, Service Bus Standard), key and payload schema examples and the 14 day example (not confirmed in fetched pages).
Method: documentation only; no commands were run.

## Verify
- [ ] Send a payload well over the broker limit end to end.
- [ ] Redrive a DLQ message after the longest planned delay: payload still present.
- [ ] Tampered object fails hash check and is dead-lettered.
