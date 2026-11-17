---
id: computing-software.cloud-infrastructure-engineering.aws.sqs-long-polling-batching-and-cost
name: sqs-long-polling-batching-and-cost
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, sqs, long-polling, short-polling, batch-actions, sqs-cost, receive-message-wait-time, wait-time-seconds, send-message-batch, delete-message-batch, empty-receives, max-number-of-messages, request-pricing, polling-strategy, messaging]
level: practitioner
status: docs-checked
description: "Cut SQS request cost and empty receives: queue-level long polling, 10-message batching on send/receive/delete, and sizing consumer polling loops so cost tracks throughput."
sources: ["https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-short-and-long-polling.html", "https://docs.aws.amazon.com/AWSSimpleQueueService/latest/APIReference/API_SendMessageBatch.html", "https://aws.amazon.com/sqs/pricing/", "https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/quotas-messages.html", "https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-visibility-timeout.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SQS long polling, batching and request cost

**Goal:** the SQS bill is proportional to messages, not to how often idle consumers ask
"anything yet?", and nobody discovers that 90% of requests were empty receives.

## 1. Where the money goes
SQS charges **per request**: every SQS action counts as a request, a request can carry 1 to 10 messages
(up to 1 MiB total), and each 64 KB chunk of a payload is billed as one request (a 1 MiB payload is 16
requests). A `ReceiveMessage` that returns nothing is still a billed request. CloudWatch
`NumberOfEmptyReceives` shows the waste; if it is a large share of `NumberOfMessagesReceived`, fix polling first.

## 2. Long polling
```bash
# queue default — every consumer that does not override gets it
aws sqs set-queue-attributes --queue-url "$Q" --attributes '{"ReceiveMessageWaitTimeSeconds":"20"}'
# per call (overrides the queue setting)
aws sqs receive-message --queue-url "$Q" --wait-time-seconds 20 --max-number-of-messages 10
```
- `WaitTimeSeconds` max is 20; long polling is in effect whenever it is greater than 0 (short polling when it
  is 0, set per call or via the queue's `ReceiveMessageWaitTimeSeconds`). Long polling queries **all** SQS
  servers (short polling samples a weighted-random subset, so it can return empty while messages exist) and
  responds as soon as at least one message is available; an empty response comes only when the wait expires.
- Set the HTTP client's socket timeout **above** the wait time so the long poll is not cut off.

## 3. Batching
`SendMessageBatch`, `DeleteMessageBatch`, `ChangeMessageVisibilityBatch` take up to 10
entries and cost one request (plus 64 KB chunks of total payload). The total payload of a batch is limited
to 1 MiB (1,048,576 bytes), the same as the single-message limit. Pattern:
```python
# producer: accumulate up to 10 entries or 1 MiB, flush on size/time
resp = sqs.send_message_batch(QueueUrl=q, Entries=[{"Id": str(i), "MessageBody": b} for i, b in enumerate(chunk)])
for f in resp.get("Failed", []):      # partial failures are per-entry, not an exception
    retry[f["Id"]] = f["Code"]         # per-entry error code, e.g. InvalidMessageContents
```
- A batch call can return HTTP 200 with some entries failed; **always check `Failed`**. Request-level
  errors (for example `BatchRequestTooLong`, `TooManyEntriesInBatchRequest`, `BatchEntryIdsNotDistinct`)
  raise instead.
- `MaxNumberOfMessages=10` on receive; if the queue has fewer, you get fewer (not padded by
  waiting, unless long polling finds more within the wait).
- Delete in batches after processing, not one `DeleteMessage` per message.
- The AWS SDK for Java offers `AmazonSQSBufferedAsyncClient` for client-side batching.

## 4. Consumer loop sizing
- Workers = concurrency you want; each worker long-polls with `MaxNumberOfMessages=10`. Idle
  cost per worker ≈ 3 requests/min (20 s waits) — 4,320/day, negligible.
- Scale workers on `ApproximateNumberOfMessagesVisible` / backlog-per-instance target tracking
  (publish a custom metric: backlog ÷ running instances, target = messages one instance can
  clear within the latency SLA).
- Do not scale on `NumberOfMessagesSent` — it tells you nothing about backlog.

## 5. Other cost levers
- Free tier: 1 million SQS requests per month (counted across all Regions except GovCloud).
- FIFO send, receive, delete and visibility-change actions are charged at FIFO rates; other requests at
  standard rates. On standard queues, requests that involve a message group ID incur both fair-queue and
  standard rates. See the SQS pricing page for current prices.
- Large payloads: store in S3 (Extended Client) instead of paying for many 64 KB chunks.

## Gotchas
- Setting `ReceiveMessageWaitTimeSeconds` on the queue changes behaviour for every existing
  consumer; one with a 10 s socket timeout will start failing — roll out with the client fix.
- Long polling does not change visibility semantics: the returned messages are still in-flight
  for `VisibilityTimeout` seconds; if the consumer crashes mid-batch all 10 reappear later.
- In-flight limit: about 120,000 messages for standard queues and 120,000 for FIFO. With short polling
  SQS returns `OverLimit` when a standard queue reaches it; with long polling it returns no error and simply
  returns no new messages until in-flight drops. Delete messages after processing.

## Verify
- [ ] `NumberOfEmptyReceives` (Sum, 1 h) drops to ≤ 5% of `NumberOfMessagesReceived` after enabling long polling.
- [ ] Requests per message (CloudWatch `NumberOfMessagesSent` vs billing usage type `Requests`) ≈ 0.3 or less with batching (send 0.1 + receive 0.1 + delete 0.1).
- [ ] A batch whose combined size exceeds 1 MiB is rejected with `BatchRequestTooLong`; an entry with invalid characters appears in `Failed` with `InvalidMessageContents` while the others succeed.

## Checked

Date 2026-10-23. Documentation release: current Amazon SQS Developer Guide, API Reference and SQS pricing page.
Confirmed: per-request billing, 64 KB chunk billing, 1 MiB per request, 1 million request free tier; long polling max 20 s and short vs long behaviour; queue attribute `ReceiveMessageWaitTimeSeconds`; batch limits (10 entries, 1 MiB total) and error names (`BatchRequestTooLong`, `TooManyEntriesInBatchRequest`, `BatchEntryIdsNotDistinct`, `InvalidMessageContents`); partial failure reporting under HTTP 200; `NumberOfEmptyReceives` metric; FIFO in-flight limit 120,000 (the old "20,000" was wrong) and the OverLimit/long-polling behaviour. Corrected: the 256 KB batch size and the 300 KB `Failed` example, which predate the 1 MiB limit.
Removed (not in docs): request-per-day estimate, SDK timeout defaults, Lambda long-polling claim, aiobotocore and temporary-queue-client remarks, FIFO-vs-standard price comparison, high-throughput FIFO price claim, VPC endpoint NAT saving, message-attribute chunk arithmetic.
Sources: https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-short-and-long-polling.html ; https://docs.aws.amazon.com/AWSSimpleQueueService/latest/APIReference/API_SendMessageBatch.html ; https://aws.amazon.com/sqs/pricing/ ; .../quotas-messages.html ; .../sqs-visibility-timeout.html

Method: documentation only; no commands were run.
