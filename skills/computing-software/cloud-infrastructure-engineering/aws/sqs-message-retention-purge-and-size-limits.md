---
id: computing-software.cloud-infrastructure-engineering.aws.sqs-message-retention-purge-and-size-limits
name: sqs-message-retention-purge-and-size-limits
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, sqs, message-retention, purge-queue, message-size, retention-period, sqs-limits]
level: practitioner
status: docs-checked
description: "Set SQS message retention, maximum message size and purge behaviour correctly: retention ranges, DLQ retention interplay, the 60-second purge window and what is lost."
sources: ["https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/quotas-messages.html", "https://docs.aws.amazon.com/AWSSimpleQueueService/latest/APIReference/API_SetQueueAttributes.html", "https://docs.aws.amazon.com/AWSSimpleQueueService/latest/APIReference/API_PurgeQueue.html", "https://docs.aws.amazon.com/AWSSimpleQueueService/latest/APIReference/API_DeleteQueue.html", "https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-dead-letter-queues.html", "https://aws.amazon.com/sqs/pricing/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SQS message retention, purge and size limits

**Goal:** choose retention and size so messages are neither silently expired nor too large,
and purge a queue without surprises.

## Retention
- `MessageRetentionPeriod`: 60 s to 1,209,600 s (14 days); default 345,600 s (4 days).
- Expired messages are deleted by SQS when retention is reached; they are not moved to a DLQ. If consumers can be
  down for a weekend, the 4-day default is the minimum; choose up to 14 days where backlog must survive.
```bash
aws sqs set-queue-attributes --queue-url "$Q" \
  --attributes MessageRetentionPeriod=1209600
```
- **DLQ interplay:** on standard queues a message keeps its original enqueue timestamp when moved
  to the DLQ, so a 4-day source plus a 4-day DLQ gives the DLQ no extra time; AWS recommends a DLQ retention
  longer than the source's. On FIFO queues the timestamp resets when moved.
- Retention changes can take up to 15 minutes to take effect and apply to messages already in the queue:
  lowering below a message's age can expire and delete existing messages. Most other attribute changes
  propagate within 60 seconds.

## Message size
- `MaximumMessageSize` is configurable from 1,024 bytes (1 KiB) to 1,048,576 bytes (1 MiB); default 1 MiB.
  A message can hold up to 10 metadata attributes.
- Bigger payloads (up to 2 GB): the Extended Client Library for Java or Python stores the payload in S3
  and sends a reference.
- Billing: each 64 KB chunk of a payload is billed as one request (a 1 MiB payload is 16 requests).

## Purge
```bash
aws sqs purge-queue --queue-url "$Q"
```
- Deletes available messages, including in-flight ones; the deletion takes up to 60 seconds and AWS recommends
  waiting 60 seconds regardless of queue size.
- A second purge within 60 seconds fails with `PurgeQueueInProgress`.
- Messages sent before the call may still be received but are deleted within the next minute; messages sent
  after the call might be deleted while the purge runs. Stop producers first, wait 60 s after the purge,
  then restart them.
- Irreversible: you cannot retrieve purged messages. For a DLQ, inspect first (for example `receive-message
  --max-number-of-messages 10 --visibility-timeout 0`), or redrive instead of purging.
- Restrict `sqs:PurgeQueue` in IAM to operators; applications do not need it.

## Gotchas
- `DeleteQueue` takes up to 60 seconds, and you must wait at least 60 seconds before creating a queue with the same name.

## Verify
- [ ] `get-queue-attributes --attribute-names All` shows intended retention and size on source and DLQ.
- [ ] DLQ retention >= source retention.
- [ ] Purge runbook says: stop producers, purge, wait 60 s, verify `ApproximateNumberOfMessages` = 0, restart.

## Checked

Date 2026-10-23. Documentation release: current Amazon SQS Developer Guide and API Reference.
Confirmed: retention 60 s to 1,209,600 s, default 345,600 s; retention change propagation (up to 15 minutes) and effect on existing messages; standard vs FIFO enqueue-timestamp behaviour in a DLQ; `MaximumMessageSize` 1,024 to 1,048,576 bytes (default 1 MiB; corrects nothing in the range but removes the "confirm" hedge); 10 attributes; 2 GB via Extended Client; 64 KB chunk billing; PurgeQueue behaviour, 60-second window and `PurgeQueueInProgress`; DeleteQueue 60-second rules.
Removed (not in docs): "no metric" remark on expiry, in-flight purge receipt-handle error text, and retention-versus-in-flight remark.
Sources: https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/quotas-messages.html ; https://docs.aws.amazon.com/AWSSimpleQueueService/latest/APIReference/API_SetQueueAttributes.html ; https://docs.aws.amazon.com/AWSSimpleQueueService/latest/APIReference/API_PurgeQueue.html ; https://docs.aws.amazon.com/AWSSimpleQueueService/latest/APIReference/API_DeleteQueue.html ; https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-dead-letter-queues.html ; https://aws.amazon.com/sqs/pricing/

Method: documentation only; no commands were run.
