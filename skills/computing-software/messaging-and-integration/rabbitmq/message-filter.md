---
id: computing-software.messaging-and-integration.rabbitmq.message-filter
name: message-filter
category: computing-software
field: messaging-and-integration
product: rabbitmq
tags: [rabbitmq, messaging, message-filter]
level: practitioner
status: docs-checked
description: "Drop unwanted messages with selective bindings or a consumer-side filter."
sources:
  - https://www.enterpriseintegrationpatterns.com/patterns/messaging/
  - https://www.rabbitmq.com/docs/exchanges
  - https://www.rabbitmq.com/docs/stream-filtering
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Message filter

**Goal:** Receive only relevant messages.

## Steps
1. Prefer narrower topic bindings so the broker filters; a pattern such as `regions.na.cities.*` matches one word in the last position and `#` matches zero or more words.
2. For filters on the body, filter in the consumer and ack the unwanted message so it is not requeued.
3. Streams filter server side in stages: a Bloom filter per chunk (publisher sets `x-stream-filter-value`, AMQP 0-9-1 consumer sets the `x-stream-filter` argument; false positives are possible, so keep a client-side check), AMQP filter expressions per message, then client-side filtering. Filter size is set by the stream argument `x-stream-filter-size-bytes`. By default messages without a filter value are not delivered to a Bloom-filtering consumer; `x-stream-match-unfiltered` true changes that.

## Failure modes
- Filtering by requeue loops messages forever.

## Verify
- Compare counts before and after the filter.

## Checked
2026-11-09. Message Filter named on the EIP messaging index. Confirmed on the Exchanges page (topic wildcard behaviour) and the Stream Filtering page (Bloom filter stage, false positives, `x-stream-filter-value`, `x-stream-filter`, `x-stream-filter-size-bytes`, `x-stream-match-unfiltered`, AMQP filter expressions, client-side stage). The earlier "unconfirmed per version" Bloom filter claim is now confirmed. The requeue-loop warning is design advice. Removed: the version note.
Method: documentation only; no commands were run.
