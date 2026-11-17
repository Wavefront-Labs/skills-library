---
id: computing-software.messaging-and-integration.rabbitmq.claim-check
name: claim-check
category: computing-software
field: messaging-and-integration
product: rabbitmq
tags: [rabbitmq, messaging, claim-check]
level: advanced
status: docs-checked
description: "Store large payloads externally and send only a reference to keep messages small."
sources:
  - https://www.enterpriseintegrationpatterns.com/patterns/messaging/
  - https://www.rabbitmq.com/docs/configure
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Claim check

**Goal:** Avoid large messages.

## Steps
1. Store the blob (object store), publish a message with the object key and a checksum.
2. The consumer fetches the blob, then processes it; delete blobs by lifecycle rule or TTL once no consumer needs them.
3. Keep messages small. The broker setting `max_message_size` is the largest allowed payload in bytes (default 16777216, which is 16 MiB; maximum 536870912, which is 512 MiB); larger messages are rejected with a channel exception.

## Failure modes
- Orphaned blobs without cleanup.
- Deleting the blob before a redelivered message is processed.

## Verify
- Check a large file path end to end.

## Checked
2026-11-09. Claim Check is named on the EIP messaging index. Confirmed on the RabbitMQ Configuration page: `max_message_size` meaning, default 16777216 and maximum 536870912. Corrected: the draft said the default is 128 MiB, which the page contradicts (16 MiB). Removed: the "unconfirmed" marker and the version note.
Method: documentation only; no commands were run.
