---
id: computing-software.cloud-infrastructure-engineering.aws.sqs-fifo-deduplication-and-message-groups
name: sqs-fifo-deduplication-and-message-groups
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, sqs, fifo-queue, message-group-id, deduplication, high-throughput-fifo, content-based-deduplication, message-deduplication-id, ordering, exactly-once-processing, fifo-throughput, sequence-number, lambda-fifo, messaging]
level: practitioner
status: docs-checked
description: "Design SQS FIFO message groups and deduplication IDs so ordering is preserved per key, throughput scales with group count, and the 5-minute dedup window does not drop legitimate retries."
sources: ["https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/using-messagededuplicationid-property.html", "https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/using-messagegroupid-property.html", "https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/high-throughput-fifo.html", "https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/quotas-messages.html", "https://docs.aws.amazon.com/AWSSimpleQueueService/latest/APIReference/API_SetQueueAttributes.html", "https://docs.aws.amazon.com/lambda/latest/dg/services-sqs-errorhandling.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SQS FIFO: deduplication and message groups

**Goal:** strict ordering where it matters (per order, per device, per tenant), parallelism
everywhere else, and no silent message loss from the deduplication window.

## 1. The two IDs and what they actually do
| Property | Scope | Effect |
|---|---|---|
| `MessageGroupId` (required) | per message | Messages in the same group are processed one at a time, in strict order; while one is in flight, later messages of that group are not delivered until it is deleted or its visibility timeout expires. Different groups proceed independently. |
| `MessageDeduplicationId` (or content-based) | per queue, 5 min | A second send with the same ID inside the 5-minute window is **acknowledged but not delivered**; SQS keeps tracking the ID even after the first message has been received and deleted. |

Create the queue:
```bash
aws sqs create-queue --queue-name orders.fifo --attributes '{
  "FifoQueue":"true","ContentBasedDeduplication":"false",
  "DeduplicationScope":"messageGroup","FifoThroughputLimit":"perMessageGroupId",
  "VisibilityTimeout":"60","RedrivePolicy":"{\"deadLetterTargetArn\":\"arn:aws:sqs:<REGION>:<ACCOUNT_ID>:orders-dlq.fifo\",\"maxReceiveCount\":\"5\"}"}'
aws sqs send-message --queue-url "$Q" --message-group-id order-1234 \
  --message-deduplication-id "order-1234-evt-9f2c" --message-body '{"orderId":"1234","event":"paid"}'
```

## 2. Choosing MessageGroupId
- Group = the unit that needs ordering, nothing broader. `tenantId` forces every tenant's
  traffic through one lane; `orderId` gives thousands of lanes. Throughput is **per group**:
  a group with a stuck consumer blocks only that group.
- One hot group = serial processing at the consumer's speed. If a single entity really
  produces thousands of msg/s, FIFO is the wrong tool (or shard the key: `order-1234-0..3`
  and accept ordering only within shards).
- With Lambda on a FIFO queue the maximum batch size is 10 and the batching window does not apply. With
  partial batch responses (`ReportBatchItemFailures`), the function should stop at the first failure and
  return all failed **and unprocessed** messages in `batchItemFailures` to preserve order.
- A message in flight blocks later messages of its group until it is deleted or its visibility timeout
  expires; it does not lock the group indefinitely.

## 3. Deduplication — the window that bites
- Explicit `MessageDeduplicationId`: use a **business idempotency key** (`orderId + eventType
  + version`), not a random UUID (a UUID per attempt dedups nothing) and not just `orderId`
  (the second legitimate event for that order within 5 minutes is dropped).
- `ContentBasedDeduplication=true`: SHA-256 of the **body only** — attributes are ignored, so
  two "heartbeat" messages with identical bodies 2 minutes apart collapse to one. Add a
  timestamp/sequence to the body if every message must be delivered.
- Producer retries after a network timeout are safe: a repeat with the same ID is acknowledged and not
  delivered again. This is the intended use.
- Deduplication is at *send* time; it does not dedupe deliveries to the consumer (a consumer that
  crashes after processing still sees a redelivery: keep the consumer idempotent too).
- `DeduplicationScope=messageGroup` is required for high-throughput mode and means the same
  dedup ID in two different groups counts as two messages.

## 4. Throughput tiers
- Default (non-high-throughput) FIFO: 300 transactions per second per partition per API action
  (`SendMessage`, `ReceiveMessage`, `DeleteMessage`); with batches of 10, up to 3,000 messages per second.
- High throughput needs **both** `DeduplicationScope=messageGroup` and `FifoThroughputLimit=perMessageGroupId`.
  Request-rate limits then depend on the Region, for example up to 70,000 TPS non-batched in US East
  (N. Virginia), US West (Oregon) and Europe (Ireland), 19,000 in US East (Ohio) and Frankfurt, 2,400 in other
  Regions; batching raises the message rate tenfold. Increase the number of message groups to use the
  capacity; AWS recommends group IDs with many distinct values. Check the quotas page for current figures.
- SQS hashes each message group ID to a partition; each partition supports up to 3,000 messages per second
  with batching or 300 without.

## Gotchas
- `MessageGroupId` is required on FIFO (the send fails without it); `MessageGroupId` is up to 128
  characters. On standard queues it is accepted as a fair-queue tenant ID with different semantics.
- Delay: only **queue-level** `DelaySeconds` works on FIFO; per-message timers are not supported.
- A FIFO DLQ must itself be FIFO. AWS advises against a DLQ on a FIFO queue when exact order must be
  preserved, because moving a message out of sequence changes the order of operations.
- Regional high-throughput ceilings change; check the message quotas page before capacity planning.

## Verify
- [ ] Sending the same `MessageDeduplicationId` twice within 5 minutes delivers one message; the repeat is acknowledged but not delivered.
- [ ] Two groups processed concurrently while a third group with a failing message does not block them.
- [ ] `aws sqs get-queue-attributes --attribute-names All` shows `DeduplicationScope=messageGroup` and `FifoThroughputLimit=perMessageGroupId` when high throughput was intended.
- [ ] Load test with 1 group vs 100 groups shows throughput scaling roughly linearly with groups until the per-queue quota.

## Checked

Date 2026-10-23. Documentation release: current Amazon SQS Developer Guide and API Reference, Lambda Developer Guide.
Confirmed: 5-minute deduplication window and that duplicates are acknowledged but not delivered (and the ID is tracked after delete); content-based deduplication hashes the body only (SetQueueAttributes reference); attribute names `FifoQueue`, `ContentBasedDeduplication`, `DeduplicationScope`, `FifoThroughputLimit` and the two values needed for high throughput; group semantics (one at a time, strict order, in-flight blocking); 300 TPS per partition and 3,000 with batching; regional high-throughput TPS; FIFO Lambda batch size 10 and partial-batch guidance; FIFO DLQ must be FIFO; no per-message timers on FIFO; `MessageGroupId` 128 characters.
Removed (not in docs): returned `SequenceNumber` on duplicates, Lambda scaling-by-groups claim, `MissingParameter` error name, S3 notification and SNS FIFO fan-out claims, one-group 300 msg/s claim, "interval is fixed".
Sources: https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/using-messagededuplicationid-property.html ; .../using-messagegroupid-property.html ; .../high-throughput-fifo.html ; .../quotas-messages.html ; .../APIReference/API_SetQueueAttributes.html ; https://docs.aws.amazon.com/lambda/latest/dg/services-sqs-errorhandling.html

Method: documentation only; no commands were run.
